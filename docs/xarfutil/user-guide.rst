User Guide
----------

The following paragraphs show some examples of using the `xarfutil`
command line tool for generating valid X-ARF reports.

Generating Reports
~~~~~~~~~~~~~~~~~~
In this first example, all required parameters for generating a X-ARF report are
specified directly at command line. Using the `--output-yaml` parameter, the
validated report data is printed to `stdout` in YAML format.

.. note::

    For better readablity, the command line was wrapped.

**Example:**

::

    $ python xarfutil.py --evidence 'sample evidence data' --greeting 'greeting text here' \
        --schema-url 'http://xarf.org/schema/abuse_login-attack_0.1.2.json' \
        --schema-cache '/tmp/' --reported-from 'xarf-reports@example.com' \
        --category 'abuse' --report-type 'login-attack' --report-id '1234567' \
        --date 'Feb  3 2014 02:13:35 +0100' --source '83.169.54.26' \
        --source-type 'ip-address' --attachment 'text/plain' --service 'ssh' \
        --port 22 --output-yaml
    evidence: sample evidence data
    machine_readable:
      Attachment: text/plain
      Category: abuse
      Date: Feb  3 2014 02:13:35 +0100
      Port: 22
      Report-ID: '1234567'
      Report-Type: login-attack
      Reported-From: xarf-reports@example.com
      Schema-URL: http://xarf.org/schema/abuse_login-attack_0.1.2.json
      Service: ssh
      Source: 83.169.54.26
      Source-Type: ip-address
      User-Agent: pyxarf 0.0.1

.. note::

    Printing the plain X-ARF report does not include `greeting` data,
    as this is email specific. Use `--output-email` to preview all
    generated data, including `greeting`, as a raw email.


The second example shows generating a valid X-ARF report by reading all
required data from input files. `evidence.txt` and `greeting.txt` contain
some sample text and are omitted for readability.

**Example:**

::

    $ cat test.yaml
    Attachment: text/plain
    Category: abuse
    Date: Feb  3 2014 02:13:35 +0100
    Port: 22
    Report-ID: '1234567'
    Report-Type: login-attack
    Reported-From: xarf-reports@example.com
    Schema-URL: http://xarf.org/schema/abuse_login-attack_0.1.2.json
    Service: ssh
    Source: 83.169.54.26
    Source-Type: ip-address
    User-Agent: pyxarf 0.0.1(pyxarf)sb
    $ xarfutil.py --file-evidence evidence.txt --file-machine-readable test.yaml \
    --file-greeting greeting.txt --output-yaml
    evidence: 'EVIDENCE SAMPLE'
    machine_readable:
      Attachment: text/plain
      Category: abuse
      Date: Feb  3 2014 02:13:35 +0100
      Port: 22
      Report-ID: '1234567'
      Report-Type: login-attack
      Reported-From: xarf-reports@example.com
      Schema-URL: http://xarf.org/schema/abuse_login-attack_0.1.2.json
      Service: ssh
      Source: 83.169.54.26
      Source-Type: ip-address
      User-Agent: pyxarf 0.0.1


Sending Reports
~~~~~~~~~~~~~~~

You can directly send the generated X-ARF report by mail via `xarfutils` by setting
the correct mail options and using the command line parameter `--send-email`.

**Example:**

::

    $ python xarfutil.py --evidence 'sample evidence data' \
    --greeting 'greeting text here' \
    --schema-url 'http://xarf.org/schema/abuse_login-attack_0.1.2.json' \
    --schema-cache '/tmp/' --reported-from 'xarf@example.org' \
    --category 'abuse' --report-type 'login-attack' --report-id '1234567' \
    --date 'Feb  3 2014 02:13:35 +0100' --source '83.169.54.26' \
    --source-type 'ip-address' --attachment 'text/plain' --service 'ssh' \
    --port 22 --mail-server-host mx.example.org --mail-server-port 25 \
    --mail-from 'xarf@example.org' --mail-subject 'x-arf sample report' \
    --mail-to 'abuse@example.com' --send-email

    Report sent.


If you want to send the generated report yourself, you can also print
the raw email, using the `--output-email` switch, as shown below.

.. note::

    If you use the `--lookup-contact <xarfutil/parameters.html#lookup-contact>`_
    parameter, the report recipient is set automatically.

.. warning::

    `--lookup-contact <xarfutil/parameters.html#lookup-contact>`_ overwrites
    `--mail-to <xarfutil/parameters.html#mail-to>`_.


**Example:**

::

    $ python xarfutil.py --evidence 'sample evidence data' \
    --greeting 'greeting text here' \
    --schema-url 'http://xarf.org/schema/abuse_login-attack_0.1.2.json' \
    --schema-cache '/tmp/' --reported-from 'xarf@example.org' \
    --category 'abuse' --report-type 'login-attack' --report-id '1234567' \
    --date 'Feb  3 2014 02:13:35 +0100' --source '83.169.54.26' \
    --source-type 'ip-address' --attachment 'text/plain' --service 'ssh' \
    --port 22 --mail-server-host mx.example.org --mail-server-port 25 \
    --mail-from 'xarf@example.org' --mail-subject 'x-arf sample report' \
    --mail-to 'abuse@example.com' --output-email

    Content-Type: multipart/mixed; boundary="===============8786047389680449662=="
    MIME-Version: 1.0
    From: xarf@example.org
    Subject: x-arf sample report
    To: abuse@example.com
    X-XARF: PLAIN
    Auto-Submitted: auto-generated

    --===============8786047389680449662==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    greeting text here
    --===============8786047389680449662==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    Attachment: text/plain
    Category: abuse
    Date: Feb  3 2014 02:13:35 +0100
    Port: 22
    Report-ID: '1234567'
    Report-Type: login-attack
    Reported-From: xarf@example.org
    Schema-URL: http://xarf.org/schema/abuse_login-attack_0.1.2.json
    Service: ssh
    Source: 83.169.54.26
    Source-Type: ip-address
    User-Agent: pyxarf 0.0.1

    --===============8786047389680449662==
    Content-Type: text/plain; charset="utf-8"
    MIME-Version: 1.0
    Content-Transfer-Encoding: quoted-printable

    sample evidence data
    --===============8786047389680449662==--

.. warning::

   If you don't specify `--mail-from`, `--mail-to` and `--mail-subject`, the
   appropriate header fields will be empty in the raw email.


Handling Errors
~~~~~~~~~~~~~~~

If a supplied value does not comply with the specified X-ARF schemata,
a detailed error message is shown.

**Example:**

::

    $ python xarfutil.py --evidence 'sample evidence data' \
    --greeting 'greeting text here' \
    --schema-url 'http://xarf.org/schema/abuse_login-attack_0.1.2.json' \
    --schema-cache '/tmp/' --reported-from 'xarf-reports@example.com' \
    --category 'abuse' --report-type 'login-attack' --report-id '1234567' \
    --date 'Feb  3 2014 02:13:35 +0100' --source '83.169.54.26' \
    --source-type 'foo' --attachment 'text/plain' --service 'ssh' \
    --port '22' --output-yaml
    error: validation failed! reason(s):
    Source-Type 'foo' is not one of [u'ipv4', u'ipv6', u'ip-address']
