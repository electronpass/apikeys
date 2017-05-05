#!/usr/bin/python3

import sys
import os
import json

enc_file, passwd, template, output_file_name = sys.argv[1:5]
print("Compiling", template, "with data from", enc_file, "to", output_file_name)
print("Decrypting ...")
st = os.system("gpg -d --batch --passphrase {} -o keys.json {}".format(passwd, enc_file))
if st != 0:
    print("Decryption failed, exiting!")
    sys.exit(1)

print("Opening files ...")
with open("keys.json", "r") as keysfile, open(template, "r") as tplfile, open(output_file_name, "w") as outfile:
    print("Loading json ...")
    keysobj = json.loads(keysfile.read())

    print("Compiling template")
    result = ""
    for line in tplfile:
        var_active = False
        var_name = ""
        current_line = ""
        for char in line:
            if char == "#":
                break
            elif char == "%":
                if var_active:
                    current_line += keysobj[var_name]
                else:
                    var_name = ""
                var_active = not var_active
            elif var_active:
                var_name += char
            else: current_line += char
        if current_line != "": result += current_line.rstrip() + "\n"

    if result == "":
        print("Result is empty!")
    else:
        print("Writing result to", output_file_name)
        outfile.write(result)


print("Cleaning up ...")
os.remove("keys.json")
