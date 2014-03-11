#!/bin/bash
sed -i '/ids.py/d' /etc/crontab 
if [$1 !=""]; then
  return 0
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

echo "*/2 * * * *  $DIR/ids.py " >> /etc/crontab
