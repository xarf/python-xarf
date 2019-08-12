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
