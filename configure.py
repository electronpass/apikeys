#!/usr/bin/python3

import sys
import subprocess
import json
import re

if len(sys.argv) != 4:
    print('Usage:\nconfigure.py [encrypted file] [password] [output file] ')
    sys.exit()

encrypted_file, password, output_file = sys.argv[1:]

print('Decrypting {}'.format(encrypted_file))

# Call gpg, decrypted file will be stored in completed_process.stdout
completed_process = subprocess.run(['gpg', '-d', '--batch', '--passphrase', password, encrypted_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if completed_process.returncode != 0:
    print(completed_process.stdout, '\n', completed_process.stderr, '\nDecryption failed, exiting')
    sys.exit(1)

api_keys = json.loads(completed_process.stdout)

print('Keys to fill: ' + ', '.join(api_keys.keys()))

# Create a dict with @key_name@ for keys
patterns_dict = dict()
for key_name in api_keys.keys(): patterns_dict['@{}@'.format(key_name)] = api_keys[key_name]

print('Opening file {}'.format(output_file))
with open(output_file, 'r') as f:
    data = f.read()

any_matches = False

def replace(match):
    global any_matches
    any_matches = True
    print('Filled in {}'.format(match.group(0)))
    return patterns_dict[match.group(0)]

# Create regular expression which will match all dict keys
regex = re.compile('({})'.format('|'.join(map(re.escape, patterns_dict.keys()))))
# For each match, find corresponding value in dict
data = regex.sub(replace, data)

if not any_matches:
    print('No patters matched. Check your file again.')

print('Saving')
with open(output_file, 'w') as f:
    f.write(data)
print('Finished')
