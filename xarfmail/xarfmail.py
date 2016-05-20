import smtplib
from email import charset
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


charset.add_charset('utf-8', charset.SHORTEST, charset.QP)

try:
    from querycontacts import ContactFinder
    cf = ContactFinder()
except ImportError as exception:
    cf = exception


def lookup_contact(ip):
    '''
    uses querycontacts if available to lookup abuse contact(s) for given ip

    :param ip: ip to lookup abuse contact for
    :type ip: str

    :returns: list of contacts or None
    :rtype: list
    :rtype: none

    :raises: :py:class:`ImportError`

    '''
    if isinstance(cf, ImportError):
        raise cf
    else:
        return cf.find(ip)


class SMTPException(Exception): pass


class SMTP(object):

    '''
    Class for sending E-Mails via SMTP

    :param host: Mail server hostname or ip address
    :type host: str
    :param port: Port of mail server (default: 25)
    :type mail_server_port: int
    :param user: Username if SMTP auth is required
    :type user: str
    :param password: Password if SMTP auth is required
    :type password: str
    '''

    def __init__(self, host, port=25, user=None, password=None):
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def send(self, mail_from, mail_to, email):
        '''
        Send the E-Mail via SMTP to the specified mail server.
        SMTP auth supported.

        :returns: True if mail was sent successfully
        :rtype: bool

        :raises: :py:class:`SMTPException`

        '''
        smtp = smtplib.SMTP(self._host, self._port)

        if self._user and self._password:
            smtp.login(self._user, self._password)

        ret = smtp.sendmail(mail_from, mail_to, email)
        smtp.quit()

        if len(ret):
            raise SMTPException(ret)

        return True


class MultiPartMail(object):
    '''
    Base class for multipart E-Mails

    :param mail_from: Sender E-Mail address
    :type mail_from: str
    :param subject: Subject of Network Abuse Report
    :type subject: str
    :param mail_to: Recipient E-Mail address can be provided as list
        for addressing multiple recipients
    :type mail_to: str or list
    '''
    def __init__(self, mail_to, mail_from, subject, subtype):
        self._email = MIMEMultipart(subtype)
        self._email['From'] = mail_from
        self._email['Subject'] = subject

        if type(mail_to) is list:
            self._email['To'] = ','.join(mail_to)
        else:
            self._email['To'] = mail_to


class XarfMail(MultiPartMail):
    '''
    Helper class for building an X-ARF E-Mail report

    :param xarf: X-ARF object to report
    :type xarf: :py:class:`Xarf`:
    :param mail_from: Sender E-Mail address
    :type mail_from: str
    :param mail_to: Recipient E-Mail address can be provided as list
        for addressing multiple recipients
    :type mail_to: str or list
    :param subject: Subject of Network Abuse Report
    :type subject: str
    :param greeting: Human readable text which contains at least basic
        information about the reported incidenteeting text in the first
        MIME Part
    :type greeting: unicode
    '''
    def __init__(self, xarf, mail_from, mail_to, subject, greeting):
        MultiPartMail.__init__(self, mail_to, mail_from, subject, 'mixed')

        self._email['X-XARF'] = 'PLAIN'
        self._email['Auto-Submitted'] = 'auto-generated'

        self._email.attach(MIMEText(greeting, 'plain', 'utf-8'))
        self._email.attach(
            MIMEText(xarf.to_yaml('machine_readable'), 'plain', 'utf-8')
        )

        if xarf.evidence:
            self._email.attach(MIMEText(xarf.evidence, 'plain', 'utf-8'))

    def __str__(self):
        '''
        Return the entire E-Mail flattened as a string.

        :returns: raw email
        :rtype: str
        '''
        return self._email.as_string()

    def to_string(self):
        '''
        Return the entire E-Mail flattened as a string.

        :returns: raw email
        :rtype: str
        '''
        return str(self)
