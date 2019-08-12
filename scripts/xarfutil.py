#! /usr/bin/env python
'''
:copyright: (c) 2014 by abusix GmbH
:license: Apache2, see LICENSE.txt for more details.
'''
from __future__ import print_function

import logging

from sys import exit, argv
from argparse import ArgumentParser, FileType, SUPPRESS
from pyxarf import Xarf
from pyxarf.exceptions import MissingParameterError, ValidationError
from xarfmail import SMTP, XarfMail, lookup_contact
import yaml

class Xarfutil(object):
    '''
    helper class for interaction with pyxarf


    '''
    def __init__(self):
        '''
        handles command line parser initialization


        '''
        self.xarf_args = {}
        self._groups = {}

        self._parser = ArgumentParser(
            description='xarfutil - xarf command line utility',
            argument_default=SUPPRESS,
        )
        self._add_arguments(self._parser)

        (self.args, self._extra_args) = self._parser.parse_known_args()
        self.args = vars(self.args)

        if 'args' in self.args: # move args= to extra_args
            self._extra_args.insert(1, self.args.pop('args')[0])

        # make sure parameter mode is not used together with file mode
        self._handle_arg_conflicts(
            ignore_groups=('mail options','output options')
        )

        self._check_file_parameters()

        # file mode was used
        if 'machine_readable' in self.xarf_args:
            self.xarf = Xarf.from_machine_readable
            return
        else: # parameter mode used
            self.xarf = Xarf

        for parameter in self._groups['parameter mode']:
            if parameter in self.args:
                self.xarf_args[parameter] = self.args[parameter]

        # convert foo=bar, bleh=blub to dict
        self._extra_args_to_dict()
        # .args contains all args
        self.args.update(self._extra_args)
        # .xarf_args contains only xarf related args
        self.xarf_args.update(self._extra_args)

    def _add_arguments(self, parser):
        '''
        configures the argument parser for handling
        all command line options

        :param parser: handle to ArgumentParser
        :type parser: :py:class:`ArgumentParser`:

        '''
        parser.add_argument('--debug', action='store_true',
            help='enable debug mode',
        )
        parser.add_argument('--send-email', action='store_true',
            help='generate and send report by mail',
        )
        parser.add_argument('--lookup-contact', action='store_true',
            help='automatically lookup abuse contact with querycontacts'
        )

        group_1 = parser.add_argument_group(
            'parameter mode',
            'read report data from parameters (conflicts with file mode)'
        )
        self._add_group_argument(group_1, '--greeting',
            type=str, metavar='<string>',
            help='greeting text (xarf part 1, only for mail generation)'
        )
        self._add_group_argument(group_1, '--evidence',
            type=str, metavar='<string>',
            help='evidence text (xarf part 2)'
        )
        self._add_group_argument(group_1, '--schema-url',
            type=str, metavar='<url>',
            help='url of json schema'
        )
        self._add_group_argument(group_1, '--schema-cache',
            type=str, metavar='<path>',
            help='path for caching schemas'
        )
        self._add_group_argument(group_1, '--reported-from',
            type=str, metavar='<email>',
            help='from email address of reporter'
        )
        self._add_group_argument(group_1, '--category',
            type=str, metavar='<string>',
            help='report category'
        )
        self._add_group_argument(group_1, '--report-type',
            type=str, metavar='<string>',
            help='report type'
        )
        self._add_group_argument(group_1, '--report-id',
            type=str, metavar='<string>',
            help='report id'
        )
        self._add_group_argument(group_1, '--date',
            type=str, metavar='<timestamp>',
            help='date of report'
        )
        self._add_group_argument(group_1, '--source',
            type=str, metavar='<ip>',
            help='source of report'
        )
        self._add_group_argument(group_1, '--source-type',
            type=str, metavar='<string>',
            help='type of source'
        )
        self._add_group_argument(group_1, '--attachment',
            type=str, metavar='<mime-type>',
            help='attachment mime-type'
        )
        self._add_group_argument(group_1, 'args', nargs='*',
            help='additional arguments, dependent on json schema'
        )

        group_2 = parser.add_argument_group(
            'file mode',
            'read report data from input files (conflicts with parameter mode)'
        )
        self._add_group_argument(group_2, '--file-evidence',
            type=FileType('r'), metavar='<path>',
            help='file with evidence data (xarf part 3)'
        )
        self._add_group_argument(group_2, '--file-machine-readable',
            type=FileType('r'), metavar='<path>',
            help='file with machine readable data (xarf part 2)'
        )
        self._add_group_argument(group_2, '--file-greeting',
            type=FileType('r'), metavar='<path>',
            help='file with greeting text (xarf part 1)'
        )

        group_3 = parser.add_argument_group(
            'output options',
            'various settings for printing validated data to stdout'
        )
        self._add_group_argument(group_3, '--output-json',
            action='store_true',
            help='print validated xarf report in json format'
        )
        self._add_group_argument(group_3, '--output-yaml',
            action='store_true',
            help='print validated xarf report in yaml format'
        )
        self._add_group_argument(group_3, '--output-email',
            action='store_true',
            help='print validated xarf report as raw email'
        )

        group_4 = parser.add_argument_group(
            'mail options', 'options when directly sending reports by email'
        )
        self._add_group_argument(group_4, '--mail-server-host',
            type=str, metavar='<hostname>',
            help='mail server ip or hostname'
        )
        self._add_group_argument(group_4, '--mail-server-port',
            type=str, metavar='<port>',
            help='mail server port'
        )
        self._add_group_argument(group_4, '--mail-server-user',
            type=str, metavar='<username>',
            help='mail server username'
        )
        self._add_group_argument(group_4, '--mail-server-pass',
            type=str, metavar='<password>',
            help='mail server password'
        )
        self._add_group_argument(group_4, '--mail-from',
            type=str, metavar='<from>',
            help='sender of report'
        )
        self._add_group_argument(group_4, '--mail-subject',
            type=str, metavar='<subject>',
            help='subject of report'
        )
        self._add_group_argument(group_4, '--mail-to',
            type=str, metavar='<recipient>',
            help='recipient of report'
        )

    def _check_file_parameters(self):
        '''
        checks if file mode command line arguments are used and reads
        the specified files to the corresponding variables

        '''
        file_handles = self._get_settings('file mode')

        if any(f in self.args for f in file_handles):
            if 'file_machine_readable' not in self.args:
                exit(
                    'error: --file-machine-readable is required with file mode'
                )

            if 'file_greeting' in self.args:
                self.args['greeting'] = file_handles[
                    'file_greeting'].read()

            if 'file_evidence' in self.args:
                self.xarf_args['evidence'] = file_handles[
                    'file_evidence'].read()

            try:
                self.xarf_args['machine_readable'] = yaml.load(
                    file_handles['file_machine_readable']
                )
            except yaml.scanner.ScannerError as e:
                exit('error: --file-machine-readable does not specify a valid '
                     'json or yaml file:\n%s' % e)

    def _add_group_argument(self, group, *args, **kwargs):
        '''
        wrapper function for :py:func:`add_argument` of
        ArgumentParser for saving group assignment in self._groups

        :param group: handle of group object
        :type group: py:func:`ArgumentParser` group object
        :param args: args of add_argument call
        :type args: list
        :param kwargs: kwargs of add_argument call
        :type kwargs: dict

        '''
        title = group.title

        arg = args[0].lstrip('-').replace('-', '_')
        if arg != 'args':
            if title not in self._groups:
                self._groups[title] = [arg]
            else:
                self._groups[title].append(arg)

        group.add_argument(*args, **kwargs)

    def _extra_args_to_dict(self):
        '''
        converts foo=bar style command line arguments to a dict

        '''
        extra_args = {}

        for i in range(0, len(self._extra_args), 2):
            key = self._extra_args[i].lstrip('-')
            try:
                value = self._cast_value(self._extra_args[i+1])
            except IndexError: # invalid parameter gets dropped
                continue
            extra_args[key] = value
        self._extra_args = extra_args

    def _cast_value(self, value):
        '''
        command line parameters are always strings, but some xarf
        schemas require int or float type arguments. this function
        tries to cast every command line value to it's real type

        :param value: value to cast
        :type value: object

        :returns: value as int, if it's an integer
        :rtype: int
        :returns: value as float, if it's a float
        :rtype: float
        :returns: value as int, if it's an integer
        :rtype: int

        '''
        try:
            if int(value) == float(value):
                return int(value)
        except:
            try:
                return float(value)
            except:
                return str(value)

    def _handle_arg_conflicts(self, ignore_groups):
        '''
        makes sure that all command line argument groups which are not
        passed to this function via the ignore_groups parameter conflict

        :param ignore_groups: groups which are allowed to conflict
        :type ignore_groups: tuple

        '''
        group_match = None
        for group in self._groups:
            if group in ignore_groups:
                continue
            for arg in self._groups[group]:
                arg = arg.replace('-', '_')
                if arg in self.args:
                    if not group_match:
                        group_match = group
                    elif group != group_match:
                        exit(
                            'error: parameters from group "%s" conflict with '
                            'group "%s"!' % (group, group_match)
                        )

    def _get_settings(self, group):
        '''
        returns all settings of the specified argument group

        :param group: name of argument group
        :type group: str

        :returns: settings
        :rtype: dict

        '''
        settings = {}
        if group in self._groups:
            for setting in self._groups[group]:
                if setting in self.args:
                    settings[setting] = self.args[setting]
        return settings

    def get_mail_to(self):
        mail_settings = self.get_mail_settings()
        mail_to = None
        if 'mail_to' in mail_settings:
            mail_to = mail_settings['mail_to']
        if 'lookup_contact' in util.args and \
                report.machine_readable['Source-Type'][:2] == 'ip':
            try:
                mail_to = lookup_contact(report.machine_readable['Source'])
            except ImportError:
                raise
            except:
                pass
        if not mail_to:
            exit("You have to supply a to mail address either by using --mail-to or --lookup-contact")
        return mail_to

    def to_mail(self, report, mail_to=None):
        '''
        returns the raw email of the specified xarf report_obj

        :param report: xarf report object
        :type report: :py:class:`Xarf`: object

        :returns: raw mail representation of xarf report
        :rtype: str

        '''
        greeting = ''

        if not mail_to:
            mail_to = self.get_mail_to()

        mail_settings = self.get_mail_settings()
        mail_from = mail_settings['mail_from']
        subject = mail_settings['mail_subject']

        if 'greeting' in util.args:
            greeting = util.args['greeting']


        self.mail_obj = XarfMail(report, mail_from, mail_to, subject, greeting)
        return str(self.mail_obj)

    def get_report(self, report):
        '''
        returns the report in the format specified with the --output-*
        command line switch

        :param report: xarf report object
        :type report: :py:class:`Xarf`: object

        :returns: json representation of xarf report
        :rtype: str
        :returns: yaml representation of xarf report
        :rtype: str
        :returns: raw mail representation of xarf report
        :rtype: str

        :raises: :py:class:`ValidationError`: if schema validation failed

        '''
        formats = {
            'output_json': (report.to_json, {}),
            'output_yaml': (report.to_yaml, {}),
            'output_email': (self.to_mail, {'report': report}),
        }
        try:
            for format in formats:
                if format in self.args:
                    func, args = formats[format]
                    return func(**args)
            else:
                return report.to_json()
        except ValidationError as e:
            exit('error: validation failed! reason(s):\n%s' % e)

    def print_help(self):
        '''
        shows the dynamically built help of :py:class:`ArgumentParser`:

        '''
        if self._parser:
            self._parser.print_help()

    def get_mail_settings(self):
        '''
        returns all mail option settings

        :returns: output of :py:func:`_get_settings`:
        :rtype: dict

        '''
        return self._get_settings('mail options')

    def get_file_handles(self):
        '''
        returns all file mode settings

        :returns: output of :py:func:`_get_settings`:
        :rtype: dict

        '''
        return self._get_settings('file mode')

if __name__ == '__main__':
    '''
    main function with primary application logic and error handling.
    uses :py:class:`Xarfutil`: helper class for wrapping all calls
    to :py:class:`pyxarf.Xarf`:

    '''
    util = Xarfutil()

    if len(argv) == 1:
        exit(util.print_help())

    try:
        report = util.xarf(**util.xarf_args)
    except MissingParameterError as e:
        exit('error: %s\nadd missing parameter(s) with --%s'
            % (e, ' --'.join(e.missing_parameters).replace('_', '-'))
        )
    except ValidationError as e:
        exit('error: validation failed! reason(s):\n%s' % e)

    if 'send_email' in util.args:
        mail_to = util.get_mail_to()
        raw_email = util.to_mail(report, mail_to)

        mail_settings = util.get_mail_settings()
        mail_from = mail_settings['mail_from']
        username = None
        password = None

        if 'mail_server_user' in mail_settings and\
                'mail_server_pass' in mail_settings:
            username = mail_settings['mail_server_user']
            password = mail_settings['mail_server_pass']

        smtp_server = SMTP(
            mail_settings['mail_server_host'],
            mail_settings['mail_server_port'],
            username,
            password,
        )

        try:
            smtp_server.send(mail_from, mail_to, raw_email)
        except:
            exit('Something went wrong while sending the Report.')
        else:
            exit('Report sent.')
    else:
        print(util.get_report(report))

