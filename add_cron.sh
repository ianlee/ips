#!/bin/bash
sed -i '/ids.py/d' /etc/crontab 


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

echo "*/2 * * * *  $DIR/ids.py " >> /etc/crontab
