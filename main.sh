x=$((5*60))

y=$(cat /var/log/secure | grep "Failed password for" | awk -v v="$(date "+%s" -d "$1 $2 $3")" '{printf "%s %s\n",$11 ,v};' )
echo $y

#date "+%s" -d "Mar 6 01:01:01" 

# this variable you could customize, important is convert to seconds. 
# e.g 5days=$((5*24*3600))
   #here we take 5 mins as example
logfile="/var/log/secure"
# this line get the timestamp in seconds of last line of your logfile
#last=$(tail -n1 $logfile|awk -F'[][]' '{ gsub(/\//," ",$2); sub(/:/," ",$2); "date +%s -d \""$2"\""|getline d; print d;}' )

#this awk will give you lines you needs:
#awk -F'[][]' -v last=$last -v x=$x '{ gsub(/\//," ",$2); sub(/:/," ",$2); "date +%s -d \""$2"\""|getline d; if (last-d<=x)print $1 "[" $2 "]" $3 }' $logfile  
