#!/bin/bash
sed '/ids.py/d' /etc/crontab 

if [$# -gt 0 && $1 !=""]; then
	exit
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

echo "*/2 * * * *  $DIR/ids.py " >> /etc/crontab