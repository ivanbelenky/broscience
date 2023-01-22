
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


# `/includes`
## `img.php` 
DONE, nothing to worry, this was the place were the security bypass was located

## `header.php` 
DONE, nothing here as well, just the output of some headers present on each of the pages.

## `navbar.php`
DONE, same as header but with navbar code. Theme function is present here.

## `db_connect.php`
WORKING: trying to connect to the db despite the fact that I am receiving php errors when running the command.
pg_connect --> neverhteless I did not find/search this, it is not relevant since the port is closed and there is no luck whatsoever in checking the db despite having them credentials.


# `var/www/html`

## `register.php`

- checking
  - all fields are present
  - password not too long 
  - email valid
  - check if user exists already
  - check if email is already in use
- invokes `generate_activation_code`

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



# utils.php
- `generate_activation_code`
- `rel_time`
- theme related:
  - `get_theme`
  - `get_theme_class`
  - `set_theme` 

# once reversed 

- psql passwords, dump to csv
  - psql -h localhost -p 5432 -U dbuser -d broscience -c "\copy (SELECT * FROM users) TO '/var/www/html/users.csv' WITH CSV HEADER"
  - RangeOfMotion%777
  - iluvhorsesandgym