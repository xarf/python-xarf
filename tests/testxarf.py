#!/usr/bin/env python
# import logging
from __future__ import print_function

from pyxarf import Xarf

# logger = logging.getLogger('pyxarf')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler('/tmp/pyxarf.log') # log to file
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


report = Xarf(
    evidence='evidence data belongs here',
    schema_url='http://xarf.org/schema/abuse_login-attack_0.1.2.json',
    schema_cache='/tmp/',
    reported_from='reporter@example.com',
    category='abuse',
    report_type='login-attack',
    report_id='1231231',
    date='Jan  1 2014 02:13:35 +0100',
    source='83.169.54.26',
    source_type='ip-address',
    attachment='text/plain',
    port=22,
    service='ssh',
)

print(report.to_yaml())

test_data = {
    'Reported-From': 'reporter@example.com',
    'Category': 'abuse',
    'Report-Type': 'login-attack',
    'Service': 'ssh',
    'Date': 'Jan  1 2014 02:13:35 +0100',
    'Source-Type': 'ip-address',
    'Source': '83.169.54.26',
    'Port': 22,
    'Report-ID': '1231231',
    'Schema-URL': 'http://xarf.org/schema/abuse_login-attack_0.1.2.json',
    'Attachment': 'text/plain',
}
evidence = '''
Do you see any Teletubbies in here? Do you see a slender plastic tag
clipped to my shirt with my name printed on it? Do you see a little
Asian child with a blank expression on his face sitting outside on a
mechanical helicopter that shakes when you put quarters in it? No?
Well, that's what you see at a toy store. And you must think you're
in a toy store, because you're here shopping for an infant named Jeb.
'''

report = Xarf.from_machine_readable(test_data, evidence)
print(report.to_yaml())





