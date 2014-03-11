#!/bin/bash
sed -i '/ids.py/d' /etc/crontab 
if [ "$1" == "stop" ]; then
  return 0
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

echo "* * * * * root python $DIR/ids.py " >> /etc/crontab
