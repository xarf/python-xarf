[![PyPi Version](https://img.shields.io/pypi/v/pyxarf.svg)](https://pypi.python.org/pypi/pyxarf)
[![PyPi License](https://img.shields.io/pypi/l/pyxarf.svg)](https://pypi.python.org/pypi/pyxarf)
[![PyPi Versions](https://img.shields.io/pypi/pyversions/pyxarf.svg)](https://pypi.python.org/pypi/pyxarf)
[![PyPi Wheel](https://img.shields.io/pypi/wheel/pyxarf.svg)](https://pypi.python.org/pypi/pyxarf)

# pyxarf - easy x-arf report generation

## Introduction

pyxarf is a Python library for handling X-ARF Network Abuse Reporting.

* pyxarf: A module for creating, validating and serializing X-ARF objects.
* xarfmail: A module for sending X-ARF reports by E-Mail, with automatic Abuse Contact lookup provided by the free [querycontacts](https://pypi.python.org/pypi/querycontacts/) library.
* xarfutil: A command line client for reporting in X-ARF directly from the Shell.

For more information on the reporting format X-ARF, check out it's [offical website](http://www.xarf.org).

## Getting Started

### Installation

```bash
pip install pyxarf
```

### Calling the Script

#### Report-Generation

In this first example, all required parameters for generating a X-ARF report are
specified directly at command line. Using the `--output-yaml` parameter, the
validated report data is printed to `stdout` in YAML format.

```bash
$ xarfutil.py --evidence 'sample evidence data' --greeting 'greeting text here' \
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
```

#### Sending Reports

You can send reports using the script by adding specific parameters.

```bash
$ xarfutil.py --evidence 'sample evidence data' \
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
```

You can also lookup the abuse contact for a given IP by adding the parameter `--lookup-contact`.



## Using the API

```python
from __future__ import print_function

from pyxarf import Xarf

xarf = Xarf(
    evidence='sample evidence data',
    greeting='greeting text here',
    schema_url='http://www.xarf.org/schema/abuse_login-attack_0.1.2.json',
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

print(xarf.to_json()) # return json
print()
print(xarf.to_yaml()) # return yaml
print()
print(xarf.get_report_obj()) # return python object (dict)
```

**Output:**

```
$ python sample.py
{"machine_readable": {"Reported-From": "xarf-reports@example.com", "Report-ID": "1234567", "Category": "abuse", "Report-Type": "login-attack", "Service": "ssh", "Port": 22, "Date": "Feb  3 2014 02:13:35 +0100", "Source": "83.169.54.26", "Source-Type": "ip-address", "Attachment": "text/plain", "Schema-URL": "http://www.x-arf.org/schema/abuse_login-attack_0.1.2.json", "User-Agent": "pyxarf 0.0.5"}, "evidence": "sample evidence data"}

evidence: sample evidence data
machine_readable:
  Attachment: text/plain
  Category: abuse
  Date: Feb  3 2014 02:13:35 +0100
  Port: 22
  Report-ID: '1234567'
  Report-Type: login-attack
  Reported-From: xarf-reports@example.com
  Schema-URL: http://www.x-arf.org/schema/abuse_login-attack_0.1.2.json
  Service: ssh
  Source: 83.169.54.26
  Source-Type: ip-address
  User-Agent: pyxarf 0.0.5


{'machine_readable': {'Reported-From': 'xarf-reports@example.com', 'Report-ID': '1234567', 'Category': 'abuse', 'Report-Type': 'login-attack', 'Service': 'ssh', 'Port': 22, 'Date': 'Feb  3 2014 02:13:35 +0100', 'Source': '83.169.54.26', 'Source-Type': 'ip-address', 'Attachment': 'text/plain', 'Schema-URL': 'http://www.x-arf.org/schema/abuse_login-attack_0.1.2.json', 'User-Agent': 'pyxarf 0.0.5'}, 'evidence': 'sample evidence data'}
```


### Detecting Errors

The following example contains a error on line 17, as the specified JSON schema
definies `port` to be a integer.

```python
from __future__ import print_function

from pyxarf import Xarf

xarf = Xarf(
    evidence='sample evidence data',
    greeting='greeting text here',
    schema_url='http://www.xarf.org/schema/abuse_login-attack_0.1.2.json',
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

print(xarf.to_json())

```
**Output:**

```
$ python sample.py
Traceback (most recent call last):
  File "sample.py", line 22, in <module>
    print(xarf.to_json())
  File "/home/user/dev/python-xarf/pyxarf/xarf.py", line 362, in to_json
    return json_dumps(self.get_report_obj(part))
  File "/home/user/dev/python-xarf/pyxarf/xarf.py", line 395, in get_report_obj
    'machine_readable': self._get_validated_machine_readable(),
  File "/home/user/dev/python-xarf/pyxarf/xarf.py", line 338, in _get_validated_machine_readable
    self.machine_readable
  File "/home/user/dev/python-xarf/pyxarf/xarf.py", line 290, in _validate_schema
    ', '.join(errors)
pyxarf.exceptions.ValidationError: Port '22' is not of type 'integer'
```
