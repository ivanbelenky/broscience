Got all files
-------------
/var/www/html/
 /includes
  |-db_connect.php
  |-header.php
  |-img.php
  |-navbar.php
  |-utils.php
 index.php
 register.php
 activate.php
 login.php
 logout.php
 exercise.php
 user.php

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