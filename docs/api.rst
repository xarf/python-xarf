.. module:: pyxarf

API Documentation
-----------------

.. autoclass:: Xarf

Returns an :class:`Xarf` object when initialized with all required parameters.

**Usage:**

    >>> xarf_obj = pyxarf.Xarf(
    ... evidence='evidence data belongs here',
    ... schema_url='http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json',
    ... schema_cache='/tmp/',
    ... reported_from='reporter@example.com',
    ... category='abuse',
    ... report_type='login-attack',
    ... report_id='1231231',
    ... date='Jan  1 2014 02:13:35 +0100',
    ... source='83.169.54.26',
    ... source_type='ip-address',
    ... attachment='text/plain',
    ... port=22,
    ... service='ssh',
    ... )
    >>> type(xarf_obj)
    <class 'pyxarf.xarf.Xarf'>


__str__ method
~~~~~~~~~~~~~~

.. automethod:: Xarf.__str__()


Returns the `JSON <http://www.json.org>`_ encoded :class:`Xarf` object by calling :meth:`~Xarf.to_json`.

**Usage:**

    >>> print xarf_obj
    {"machine_readable": {"Category": "abuse", "Report-Type": "login-attack", "Service": "ssh", "Report-ID": "1231231", "Reported-From": "reporter@example.com", "Source": "83.169.54.26", "Schema-URL": "http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json", "Attachment": "text/plain", "Date": "Jan  1 2014 02:13:35 +0100", "Source-Type": "ip-address", "Port": 22, "User-Agent": "pyxarf 0.0.1"}, "evidence": "evidence data belongs here"}


add_evidence method
~~~~~~~~~~~~~~~~~~~

.. automethod:: Xarf.add_evidence(evidence)


Adds the given ``evidence`` to the current report.

**Usage:**

    >>> xarf_obj.add_evidence('this is new evidence data')

from_machine_readable method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: Xarf.from_machine_readable(machine_readable, evidence=None)

Supports initialization of :class:`Xarf` with a pre-built ``machine_readable`` object and optional ``evidence`` data.
Returns an :class:`Xarf` object.

**Usage:**

    >>> import pyxarf
    >>> data = {
    ... 'Reported-From': 'reporter@example.com',
    ... 'Category': 'abuse',
    ... 'Report-Type': 'login-attack',
    ... 'Service': 'ssh',
    ... 'Date': 'Jan  1 2014 02:13:35 +0100',
    ... 'Source-Type': 'ip-address',
    ... 'Source': '83.169.54.26',
    ... 'Port': 22,
    ... 'Report-ID': '1231231',
    ... 'Schema-URL': 'http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json',
    ... 'Attachment': 'text/plain',
    ... }
    >>> evidence = 'this is some evidence data'
    >>> xarf_obj = pyxarf.Xarf.from_machine_readable(data, evidence)
    >>> print xarf_obj
    {"machine_readable": {"Category": "abuse", "Report-Type": "login-attack", "Service": "ssh", "Report-ID": "1231231", "Reported-From": "reporter@example.com", "Source": "83.169.54.26", "Schema-URL": "http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json", "Attachment": "text/plain", "Date": "Jan  1 2014 02:13:35 +0100", "Source-Type": "ip-address", "Port": 22, "User-Agent": "pyxarf 0.0.1"}, "evidence": "this is some evidence data"}



get_report_obj method
~~~~~~~~~~~~~~~~~~~~~

.. automethod:: Xarf.get_report_obj()

Returns a Python object representation of the current report.

**Usage:**

    >>> xarf_obj.get_report_obj()
    {'machine_readable': {'Category': 'abuse', 'Report-Type': 'login-attack', 'Service': 'ssh', 'Report-ID': '1231231', 'Reported-From': 'reporter@example.com', 'Source': '83.169.54.26', 'Schema-URL': 'http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json', 'Attachment': 'text/plain', 'Date': 'Jan  1 2014 02:13:35 +0100', 'Source-Type': 'ip-address', 'Port': 22, 'User-Agent': 'pyxarf 0.0.1'}, 'evidence': 'evidence data belongs here'}



to_json method
~~~~~~~~~~~~~~

.. automethod:: Xarf.to_json()

Returns the `JSON <http://www.json.org>`_ encoded :class:`Xarf` object.

**Usage:**

    >>> xarf_obj.to_json()
    '{"machine_readable": {"Category": "abuse", "Report-Type": "login-attack", "Service": "ssh", "Report-ID": "1231231", "Reported-From": "reporter@example.com", "Source": "83.169.54.26", "Schema-URL": "http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json", "Attachment": "text/plain", "Date": "Jan  1 2014 02:13:35 +0100", "Source-Type": "ip-address", "Port": 22, "User-Agent": "pyxarf 0.0.1"}, "evidence": "evidence data belongs here"}'

to_yaml method
~~~~~~~~~~~~~~

.. automethod:: Xarf.to_yaml()

Returns the `YAML <http://www.yaml.org>`_ encoded :class:`Xarf` object.

**Usage:**

    >>> xarf_obj.to_yaml()
    "evidence: evidence data belongs here\nmachine_readable:\n  Attachment: text/plain\n  Category: abuse\n  Date: Jan  1 2014 02:13:35 +0100\n  Port: 22\n  Report-ID: '1231231'\n  Report-Type: login-attack\n  Reported-From: reporter@example.com\n  Schema-URL: http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json\n  Service: ssh\n  Source: 83.169.54.26\n  Source-Type: ip-address\n  User-Agent: pyxarf 0.0.1\n"


