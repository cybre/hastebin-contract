#!/bin/bash
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root." 1>&2
else
    cp -r HastebinContract /usr/share/
    mv /usr/share/HastebinContract/hastebin.contract /usr/share/contractor/
    chmod 755 /usr/share/HastebinContract/hastebin.py
    chmod 644 /usr/share/contractor/hastebin.contract
fi

