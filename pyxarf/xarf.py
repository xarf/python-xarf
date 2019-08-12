'''
:copyright: (c) 2014 by abusix GmbH
:license: Apache2, see LICENSE.txt for more details.

pyxarf - easy x-arf report generation

for more information see: https://docs.abusix.com/pyxarf/

'''
import logging
import requests

from os.path import isfile
from yaml import dump as yaml_dumps
from json import dumps as json_dumps, loads as json_loads
from jsonschema.validators import Draft3Validator
from .exceptions import GeneralError, MissingParameterError, ValidationError

__version__ = '0.0.5'
__useragent__ = 'pyxarf %s' % (__version__)

class Xarf(object):
    '''
    xarf report generation class

    :param evidence: raw evidence data
    :type evidence: string
    :param reported_from: source of report
    :type reported_from: string
    :param category: category of report
    :type category: string
    :param report_type: type of report
    :type report_type: string
    :param report_id: id of report
    :type report_id: string
    :param date: date of report
    :type date: string
    :param source: source of report
    :type source: string
    :param source_type: type of report source
    :type source_type: string
    :param attachment: mime type of report attachment
    :type attachment: string
    :param schema_url: url of json schema
    :type schema_url: string
    :param schema_cache: path where to cache schemas
    :type schema_cache: string
    :param kwargs: schema dependant additional parameters
    :type kwargs: dict

    '''
    # always set our own user agent
    http_headers = {
        'User-Agent': __useragent__
    }

    # mandatory schema items
    mandatory = (
        'Reported-From',
        'Category',
        'Report-Type',
        'Report-ID',
        'Date',
        'Source',
        'Source-Type',
        'Attachment',
        'Schema-URL',
    )

    def _debug(self, *messages):
        '''
        prints debug message on stdout

        :param messages: messages to log
        :type messages: tuple

        '''
        self._logger.debug(' '.join([str(x) for x in messages]))

    def __init__(
        self,
        evidence=None,
        reported_from=None,
        category=None,
        report_type=None,
        report_id=None,
        date=None,
        source=None,
        source_type=None,
        attachment=None,
        schema_url=None,
        schema_cache=None,
        **kwargs
    ):
        '''
        handles initialization with all xarf parameters as kwargs or
        full xarf reports as dict passed to param machine_readable

        '''
        self._logger = self._setup_logging()

        self.user_agent = __useragent__
        self._required_keys = {}

        self.machine_readable = None
        self.evidence = evidence
        self.schema_url = schema_url
        self.schema_cache = schema_cache

        (self.schema, self._required_keys) = self._get_schema_and_keys(
            self._get_schema_url(self.machine_readable)
        )
        self._build_machine_readable(locals(), kwargs)

    def _setup_logging(self):
        '''
        setup basic logging configuration

        :returns: logger object
        :rtype: object

        '''
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def _get_schema_and_keys(self, schema_url):
        '''
        download and convert from draft02 to draft03, also write all
        required keys to self._required_keys

        :param schema_url: url to get schema from
        :type schema_url: string

        :returns: output of :py:func:`_schema_converter`
        :rtype: tuple

        '''
        return self._schema_converter(
            self._download_schema(schema_url)
        )

    def _get_schema_url(self, machine_readable=None):
        '''
        check for schema url as parameter or in machine_readable data

        :param machine_readable: xarf machine readable part
        :type machine_readable: dict

        :returns: schema url
        :rtype: string

        :raises: :py:class:`MissingParameterError`: if schema url not defined

        '''
        if self.schema_url:
                return self.schema_url
        if machine_readable:
            if 'Schema-URL' in machine_readable:
                self.schema_url = machine_readable['Schema-URL']
                return self.schema_url
        else:
            raise MissingParameterError(
                'no schema url defined', ['schema_url']
            )

    def _build_machine_readable(self, _locals, kwargs):
        '''
        check kwargs and locals for required keys and use the given value

        :param _locals: locals of :py:func:`__init__`
        :type _locals: dict
        :param kwargs: kwargs of :py:func:`__init__`
        :type kwargs: dict

        :raises: :py:class:`MissingParameterError`: if a parameter is missing

        '''
        self.missing_parameters = []

        for key in self._required_keys:
            valid_param = key.lower().replace('-', '_')

            if valid_param in kwargs:
                self._required_keys[key] = kwargs[valid_param]
            elif valid_param in _locals:
                self._required_keys[key] = _locals[valid_param]
            else:
                self.missing_parameters.append(valid_param)
        else:
            if len(self.missing_parameters):
                raise MissingParameterError(
                    'missing required parameter(s): %s' % (
                        ', '.join(self.missing_parameters)
                    ), self.missing_parameters
                )

        self.machine_readable = self._required_keys
        self.machine_readable['User-Agent'] = __useragent__

        if not self.evidence:
            self.machine_readable['Attachment'] = 'none'

        self._debug('required schema keys', self._required_keys)

    def _download_schema(self, schema_url):
        '''
        downloads and reads schema from given url or path and returns
        it as dict

        :param schema_url: url to get schema from
        :type schema_url: string

        :returns: json schema from download or schema cache
        :rtype: dict

        :raises: :py:class:`GeneralError`: if cache access failed
        :raises: :py:class:`GeneralError`: if download of schema failed
        :raises: :py:class:`GeneralError`: if serialization failed

        '''
        schema_file = schema_url.rpartition('/')[-1]
        full_path = ''
        schema = None

        try:
            if self.schema_cache:
                full_path = '%s/%s' % (
                    self.schema_cache.rstrip('/'), schema_file
                )

                if isfile(full_path):
                    self._debug('getting schema from cache:', full_path)

                    with open(full_path, 'r') as f:
                        schema = f.read()

                    self._debug('got schema from file:', schema)
        except Exception as error:
            raise GeneralError(
                'could not get schema from cache: %s' % error
            )

        if not schema:
            try:
                self._debug('downloading schema', schema_url)
                response = requests.get(schema_url, headers=self.http_headers)
                schema = response.text

                self._debug('downloaded schema:', schema)
            except Exception as error:
                raise GeneralError(
                    'could not download schema: %s' % error
                )

        if self.schema_cache:
            with open(full_path, 'w') as f:
                f.write(schema)
        try:
            return json_loads(schema)
        except Exception as error:
            raise GeneralError(
                'could not serialize schema: %s' % error
            )

    def _validate_schema(self, schema, machine_readable):
        '''
        validates given machine_readable data against given schema
        with jsonschema draft03 validator.

        :param schema: json schema to check against
        :type schema: dict
        :param machine_readable: xarf machine readable part
        :type machine_readable: dict

        :raises: :py:class:`ValidationError`: if validation fails

        '''
        errors = []
        validator = Draft3Validator(schema)
        result = validator.iter_errors(machine_readable)

        for error in result:
            msg = '%s %s' % (error.path[0], error.message)
            errors.append(msg)

        if len(errors):
            raise ValidationError(
                ', '.join(errors)
            )

    def _schema_converter(self, schema):
        '''
        converts given schema from draft02 to draft03 as jsonschema
        does not support draft02.

        :param schema: schema to validate
        :type schema: dict

        :returns: converted schema and required keys
        :rtype: tuple

        '''

        required_keys = {}
        self._debug('before conversion:', json_dumps(schema))

        if 'properties' in schema:
            props = schema['properties']

            for item in props:
                if item == 'User-Agent':
                    continue
                if 'requires' in props[item]:
                    props[item]['dependencies'] = props[item]['requires']
                    del props[item]['requires']
                if 'optional' not in props[item]:
                    props[item]['required'] = True
                    required_keys[str(item)] = ''
                else:
                    del props[item]['optional']

        self._debug('after conversion:', json_dumps(schema))
        return (schema, required_keys)

    def _get_validated_machine_readable(self):
        '''
        validates and returns the machine readable parts

        :returns: validated machine readable data
        :rtype: dict

        '''
        self._debug(self.machine_readable)
        self._validate_schema(
                self.schema,
                self.machine_readable
            )
        return self.machine_readable

    def __str__(self):
        '''
        method for convinient usage

        :returns: output of :py:func:`to_json`
        :rtype: json

        '''
        return self.to_json()

    def to_json(self, part=None):
        '''
        returns data as json

        :param part: X-ARF object part machine_readable or evidence
        :type part: str
        :returns: json dump of xarf report
        :rtype: json

        '''
        return json_dumps(self.get_report_obj(part))

    def to_yaml(self, part=None):
        '''
        returns data as yaml

        :param part: X-ARF object part machine_readable or evidence
        :type part: str
        :returns: yaml dump of xarf report
        :rtype: yaml

        '''
        return yaml_dumps(
            self.get_report_obj(part), default_flow_style=False
        )

    def get_report_obj(self, part=None):
        '''
        returns the validated data with meta information as python dict

        :param part: X-ARF object part machine_readable or evidence
        :type part: str
        :returns: xarf report as list with both parts
        :rtype: list
        '''

        if part:
            if part == 'machine_readable':
                return self._get_validated_machine_readable()
            elif part == 'evidence':
                return self.evidence

        return {
            'machine_readable': self._get_validated_machine_readable(),
            'evidence': self.evidence,
        }

    def add_evidence(self, evidence):
        '''
        add evidence to xarf report

        :param evidence: raw evidence data
        :type evidence: string

        '''
        self.evidence = evidence

    @classmethod
    def from_machine_readable(cls, machine_readable, evidence=None):
        '''
        xarf factory to create xarf object from dict.

        :param machine_readable: xarf machine readable part
        :type machine_readable: dict
        :param evidence: raw evidence data
        :type evidence: string

        :returns: instance of :py:class:`Xarf`
        :rtype: instance

        '''
        data = {}
        for key in machine_readable:
            valid_key = key.lower().replace('-', '_')
            data[valid_key] = machine_readable[key]
        data['evidence'] = evidence
        return cls(**data)
