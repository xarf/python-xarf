#!/usr/bin/env bash
xarfutil.py --evidence 'sample evidence data' \
    --greeting 'greeting text here' \
    --schema-url 'http://www.x-arf.org/schema/abuse_login-attack_0.1.1.json' \
    --schema-cache '/tmp/' --reported-from 'xarf-reports@example.com' \
    --category 'abuse' --report-type 'login-attack' --report-id '1234567' \
    --date 'Feb  3 2014 02:13:35 +0100' --source '83.169.54.26' \
    --source-type 'ip-address' --attachment 'text/plain' --service 'ssh' \
    --port 22 --output-yaml


xarfutil.py --file-evidence evidence.txt \
    --file-machine-readable test.yaml \
    --file-greeting greeting.txt --output-yaml