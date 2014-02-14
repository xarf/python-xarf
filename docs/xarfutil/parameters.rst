Command Line Parameters
^^^^^^^^^^^^^^^^^^^^^^^

**xarfutil.py** [`--help`_] [`--debug`_] [`--send-email`_] [`--lookup-contact`_]
[`--greeting`_ <string>] [`--evidence`_ <string>] [`--schema-url`_ <url>]
[`--schema-cache`_ <path>] [`--reported-from`_ <email>]
[`--category`_ <string>] [`--report-type`_ <string>]
[`--report-id`_ <string>] [`--date`_ <timestamp>] [`--source`_ <ip>]
[`--source-type`_ <string>] [`--attachment`_ <mime-type>]
[`--file-evidence`_ <path>] [`--file-machine-readable`_ <path>]
[`--file-greeting`_ <path>] [`--output-json`_] [`--output-yaml`_]
[`--output-email`_] [`--mail-server-host`_ <hostname>]
[`--mail-server-port`_ <port>] [`--mail-server-user`_ <username>]
[`--mail-server-pass`_ <password>] [`--mail-from`_ <from>]
[`--mail-subject`_ <subject>] [`--mail-to`_ <receiptent>]
[`args`_ [`args`_ ...]]

.. seealso::

    Please check the latest `X-ARF Specification <https://github.com/abusix/
    xarf-specification>`_ for more details on each X-ARF Report Parameter,
    formats and sample values.



Optional Arguments
------------------

The arguments of this parameter group have a special purpose and do not
conflict with other parameters.


--help
~~~~~~

Show help and exit.


--debug
~~~~~~~

Activates debug mode for :mod:`pyxarf` (prints to stdout).

--send-email
~~~~~~~~~~~~

Automatically sends the generated report by Mail.

.. note::

    Settings are taken from `Mail Options`_.

--lookup-contact
~~~~~~~~~~~~~~~~

Automatically lookup abuse contact for the specified `Source` using
`querycontacts <https://pypi.python.org/pypi/querycontacts/>`_.

args
~~~~

If the specified JSON Schema requires additional parameters, not covered
by `Parameter Mode`_ options, you can add them freely to the command line,
by prefixing them with a double dash.

**Example:**

::

    $ xarfutil.py [...] --service ssh --port 22


Parameter Mode
--------------

Parameter mode provides an easy interface to specify all required settings
on command line.

.. warning::

    You can't use `Parameter Mode`_ together with `File Mode`_.

--greeting
~~~~~~~~~~

Sets the optional greeting text for the generated Mail (X-ARF MIME Part 1).

--evidence
~~~~~~~~~~

Sets the optional evidence for the generated Mail (X-ARF MIME Part 3).

--schema-url
~~~~~~~~~~~~

Specifies the Url to the current Reports `JSON Schema <http://www.json-schema.org>`_.

.. seealso::

    Check out the `X-ARF Schema Repository <https://github.com/abusix/xarf-schemata>`_
    for more information.

--schema-cache
~~~~~~~~~~~~~~

If this parameter is set, the Schema given with `--schema-url`_ is
downloaded to the specified cache path and read from this path for recurrent runs.

--reported-from
~~~~~~~~~~~~~~~

Sets the email address of the Reporter.

--category
~~~~~~~~~~

Sets the report category.

.. seealso::

    Check the `category section <https://github.com/abusix/xarf-specification/blob
    /master/xarf-specification_0.2.md#category-mandatoryonly-once>`_ of the latest
    X-ARF Specification for valid values.

--report-type
~~~~~~~~~~~~~

Sets the applicable report type.

--report-id
~~~~~~~~~~~

Sets the ID of the current report.

--date
~~~~~~

Sets the date of the report.


.. note::

    The given date string has to be :rfc:`2822` or :rfc:`3339`
    compliant.


--source
~~~~~~~~

Sets the source of abusive behavior. The format has to match the type
specified in `--source-type`_.

--source-type
~~~~~~~~~~~~~

Specifies the type of the given `--source`_.

.. note::

    In the current (0.2) version of X-ARF, only the following types
    are supported:

    * `ipv4`, `ip-address` (following :rfc:`791`)
    * `ipv6` (following :rfc:`2460`)
    * `uri` (following :rfc:`2396`)
    * `domain`
    * `email`


--attachment
~~~~~~~~~~~~

This has to be set to the applicable MIME type of the evidence data specified with `--evidence`_.
If no evidence data is set, this can be omitted.


File Mode
---------

File mode provides an advanced interface to load all required information
for generating valid X-ARF Reports from external files.

.. warning::

    You can't use `File Mode`_ together with `Parameter Mode`_.


--file-evidence
~~~~~~~~~~~~~~~

Specifies the full path to a file, containing evidence data (X-ARF MIME Part 3).

--file-machine-readable
~~~~~~~~~~~~~~~~~~~~~~~

The machine readable part of X-ARF (MIME Part 2) can be read from a file,
specified by this parameter.

.. note::

    JSON and YAML formats are supported for input.


--file-greeting
~~~~~~~~~~~~~~~

This has to be set to the file containing the greeting text, which will be
added to the generated X-ARF report mail (X-ARF MIME Part 1).

Output Options
--------------

--output-json
~~~~~~~~~~~~~

Prints the validated report to stdout in `JSON <http://www.json.org>`_ format.

--output-yaml
~~~~~~~~~~~~~

Prints the validated report to stdout in `YAML <http://www.yaml.org>`_ format.

--output-email
~~~~~~~~~~~~~~

Prints the raw report email (with headers).

Mail Options
------------

--mail-server-host
~~~~~~~~~~~~~~~~~~

Sets the SMTP server for directly sending the X-ARF report by mail.

--mail-server-port
~~~~~~~~~~~~~~~~~~

Sets the port of the SMTP server (default: 25)

--mail-server-user
~~~~~~~~~~~~~~~~~~

Optional user-name for SMTP authentication.

--mail-server-pass
~~~~~~~~~~~~~~~~~~

Optional password for SMTP authentication.

--mail-from
~~~~~~~~~~~

Sets the sender of the X-ARF report mail.

.. note::

   Both formats `"sender@example.com"` and `"Sender <sender@example.com>"` are
   supported.

--mail-subject
~~~~~~~~~~~~~~

Sets the subject of the X-ARF report mail.

--mail-to
~~~~~~~~~

Sets the receiptent of the X-ARF report mail.


