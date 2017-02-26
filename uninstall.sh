#!/bin/bash
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root." 1>&2
else
	rm /usr/share/contractor/hastebin.contract
	rm -r -f /usr/share/HastebinContract/
fi