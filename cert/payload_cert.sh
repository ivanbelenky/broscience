#!/bin/bash

openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout ./broscience.key -out ./broscience.crt -days 1 <<<"AU
    Victoria
    Melbourne
    Broscience
    Broscience
    $1
    Broscience
    " 2>/dev/null