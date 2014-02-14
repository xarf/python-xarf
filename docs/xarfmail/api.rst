.. module:: xarfmail

API Documentation
-----------------

lookup_contact function
~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: lookup_contact()

    Helper function to lookup abuse contacts using the ``querycontacts`` library.

**Usage:**

    >>> print lookup_contact('127.0.0.2')
    ['root@localhost']

class Mail
----------

.. autoclass:: XarfMail

Returns an :class:`xarfmail.XarfMail` object when initialized with all required
parameters. After initializing, printing the object returns the raw email
with the required X-ARF headers already set.


**Usage:**

::

    >>> from xarfmail import XarfMail
    >>> mail_obj = XarfMail(xarf, 'sender@example.com', 'abuse@example.org', 'this is a xarf report mail', 'this is a greeting text')
    >>> print mail_obj
    Content-Type: multipart/mixed; boundary="===============2670191234888898602=="
    MIME-Version: 1.0
    From: sender@example.com
    Subject: this is a xarf report mail
    To: abuse@example.org
    X-XARF: PLAIN
    Auto-Submitted: auto-generated

    --===============2670191234888898602==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    this is a greeting text
    --===============2670191234888898602==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    Attachment: text/plain
    Category: abuse
    Date: Feb  3 2014 02:13:35 +0100
    Port: 22
    Report-ID: '1234567'
    Report-Type: login-attack
    Reported-From: xarf-reports@example.com
    Schema-URL: http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json
    Service: ssh
    Source: 83.169.54.26
    Source-Type: ip-address
    User-Agent: pyxarf 0.0.4

    --===============2670191234888898602==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    sample evidence data
    --===============2670191234888898602==--


__str__ method
~~~~~~~~~~~~~~

.. automethod:: XarfMail.__str__()

    Prints the raw X-ARF mail


to_string method
~~~~~~~~~~~~~~~~

.. automethod:: XarfMail.to_string()

    Prints the raw X-ARF mail


class SMTP
----------

.. autoclass:: SMTP


    Helper class for sending Mails via SMTP.

send method
~~~~~~~~~~~

.. automethod:: SMTP.send()

    Sends the generated X-ARF report via ``smtplib``.



class MultiPartMail
-------------------

.. autoclass:: MultiPartMail

    Helper class for generating MultiMime Mails.

