#!/bin/bash
sed -i '/ids.py/d' /etc/crontab #remove crontab line of the program
if [ "$1" == "stop" ]; then #quit if thats the only thing we want to do
  return 0
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )" #find directory

echo "* * * * * root python $DIR/ids.py " >> /etc/crontab #add command to crontab
