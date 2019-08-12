Getting Started
---------------

The following paragraphs give a quick overview on the usage of :mod:`pyxarf`.

Basic Initialization
~~~~~~~~~~~~~~~~~~~~

**Code:**


.. code-block:: python
   :linenos:

    from pyxarf import Xarf

    xarf = Xarf(
        evidence='sample evidence data',
        greeting='greeting text here',
        schema_url='http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json',
        schema_cache='/tmp/',
        reported_from='xarf-reports@example.com',
        category='abuse',
        report_type='login-attack',
        report_id='1234567',
        date='Feb  3 2014 02:13:35 +0100',
        source='83.169.54.26',
        source_type='ip-address',
        attachment='text/plain',
        service='ssh',
        port=22,
    )

    print xarf.to_json() # return json
    print
    print xarf.to_yaml() # return yaml
    print
    print xarf.get_report_obj() # return python object (dict)

**Output:**

::

    $ python sample.py
    {"machine_readable": {"Category": "abuse", "Report-Type": "login-attack", "Service": "ssh", "Report-ID": "1234567", "Reported-From": "xarf-reports@example.com", "Source": "83.169.54.26", "Schema-URL": "http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json", "Attachment": "text/plain", "Date": "Feb  3 2014 02:13:35 +0100", "Source-Type": "ip-address", "Port": 22, "User-Agent": "pyxarf 0.0.1"}, "evidence": "sample evidence data"}

    evidence: sample evidence data
    machine_readable:
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
      User-Agent: pyxarf 0.0.1

    {'machine_readable': {'Category': 'abuse', 'Report-Type': 'login-attack', 'Service': 'ssh', 'Report-ID': '1234567', 'Reported-From': 'xarf-reports@example.com', 'Source': '83.169.54.26', 'Schema-URL': 'http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json', 'Attachment': 'text/plain', 'Date': 'Feb  3 2014 02:13:35 +0100', 'Source-Type': 'ip-address', 'Port': 22, 'User-Agent': 'pyxarf 0.0.1'}, 'evidence': 'sample evidence data'}




Detecting Errors
~~~~~~~~~~~~~~~~

The following example contains a error on line 17, as the specified JSON schema
definies `port` to be a integer.

.. code-block:: python
   :linenos:
   :emphasize-lines: 17


    from pyxarf import Xarf

    xarf = Xarf(
        evidence='sample evidence data',
        greeting='greeting text here',
        schema_url='http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json',
        schema_cache='/tmp/',
        reported_from='xarf-reports@example.com',
        category='abuse',
        report_type='login-attack',
        report_id='1234567',
        date='Feb  3 2014 02:13:35 +0100',
        source='83.169.54.26',
        source_type='ip-address',
        attachment='text/plain',
        service='ssh',
        port='22',
    )

    print xarf.to_json()


**Output:**

.. code-block:: none
   :emphasize-lines: 13

    $ python sample.py
    Traceback (most recent call last):
      File "sample.py", line 20, in <module>
        print xarf.to_json()
      File "/home/sb/mystuff/projects/pyxarf/pyxarf/xarf.py", line 347, in to_json
        return json_dumps(self.get_report_obj())
      File "/home/sb/mystuff/projects/pyxarf/pyxarf/xarf.py", line 370, in get_report_obj
        'machine_readable': self._get_validated_machine_readable(),
      File "/home/sb/mystuff/projects/pyxarf/pyxarf/xarf.py", line 325, in _get_validated_machine_readable
        self.machine_readable
      File "/home/sb/mystuff/projects/pyxarf/pyxarf/xarf.py", line 277, in _validate_schema
        ', '.join(errors)
    pyxarf.exceptions.ValidationError: Port '22' is not of type u'integer'

As seen above, a :func:`pyxarf.exceptions.ValidationError` is thrown, stating the wrong type for `port`.