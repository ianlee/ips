#!/bin/sh

# Source: http://www.pbxer.com/simple-shell-script-to-block-failed-ssh-attempts/

# scan /var/log/secure for ssh attempts
# use iptables to block the bad guys

# Looking for attempts on existing and non-existing users. For example:
# Nov  2 22:44:07 pbxer sshd[28318]: Failed password for root from 74.143.42.70 port 52416 ssh2
# Nov  3 00:06:57 pbxer sshd[31767]: Failed password for invalid user mat3 from 192.203.145.200 port 35841 ssh2

tail -1000 /var/log/secure | awk '/sshd/ && /Failed password for/ { if (/invalid user/) try[$13]++; else try[$11]++; }
END { for (h in try) if (try[h] > 4) print h; }' |
while read ip
do
	# note: check if IP is already blocked...
	/sbin/iptables -L -n | grep $ip > /dev/null
	if [ $? -eq 0 ] ; then
		echo "already denied ip: [$ip]" ;
		true	
	else
		echo "Subject: denying ip: $ip";
		logger -p authpriv.notice "*** Blocking SSH attempt from: $ip"
		/sbin/iptables -I INPUT -s $ip -j DROP
	fi
done
