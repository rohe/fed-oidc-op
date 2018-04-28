#!/usr/bin/env python3
import sys
import json

from oidcmsg.key_jar import KeyJar

keyjar = KeyJar()

keyjar.import_jwks_as_json(open(sys.argv[1]).read(), '')
print(keyjar.export_jwks_as_json(issuer=''))
