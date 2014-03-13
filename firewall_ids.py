import linecache
from datetime import datetime
import time
import subprocess, os

filepath = os.path.dirname(os.path.realpath(__file__))+"/IP_list.txt"	
#####################################################################################
# Function: 	setCutOffTime()
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	setCutOffTime()
# Returns: 		cutofftime from config file
# Notes:		cutofftime is number of seconds in which failed attempts are counted
#####################################################################################
def setCutOffTime():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 1).split()[2]) * 60
#####################################################################################
# Function: 	setDefaultTime()
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	setDefaultTime()
# Returns: 		defaultTime from config file
# Notes:		defaultTime is number of seconds a temporary ban is placed for
#####################################################################################
def setDefaultTime():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 2).split()[2]) * 60
#####################################################################################
# Function: 	setLimit()
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	setLimit()
# Returns: 		limit from config file
# Notes:		limit is number of failed attempts to be temporarily banned
#####################################################################################
def setLimit():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 3).split()[2])
#####################################################################################
# Function: 	setTotalLimit()
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	setTotalLimit()
# Returns: 		totalLimit from config file
# Notes:		totalLimit is number of failed attempts to be permanently banned
#####################################################################################
def setTotalLimit():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 4).split()[2])
#####################################################################################
# Function: 	timeExpired(epoch, cutoffTime)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	timeExpired(epoch, cutoffTime)
#							epoch		- time to check versus
#							cutoffTime	- Time limit
# Returns: 		true if cutoffTime ==0 or current time no longer within time limit
# Notes:		
#####################################################################################
def timeExpired(epoch, cutoffTime):
	return True if(cutoffTime==0 or int(datetime.now().strftime("%s")) - epoch > cutoffTime) else False 
#####################################################################################
# Function: 	appendFirewallRule(host)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	appendFirewallRule(host)
#							host		- IP address to ban
# Returns: 		N/A
# Notes:		adds rule to IP tables or if already in there then does nothing.
#####################################################################################
def appendFirewallRule(host):
	notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % host, shell=True, stdout=subprocess.PIPE).communicate()[0]
	if int(notFound): # if IP rule is not already found in iptables, append it
		os.system('logger -p authpriv.notice "*** Blocking SSH attempt from: %s"' % host)
		os.system('iptables -A INPUT -s %s -j DROP' % host)
		print "Host ", host, " added to iptables"
	else:
		print "Host ", host, " already exist in iptables"
#####################################################################################
# Function: 	removeFirewallRule(host)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	removeFirewallRule(host)
#							host		- IP address to unban
# Returns: 		N/A
# Notes:		removes rule to IP tables or if not in there then does nothing.
#####################################################################################
def removeFirewallRule(host):
	notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % host, shell=True, stdout=subprocess.PIPE).communicate()[0]
	if int(notFound): # if IP rule already does not exist, print message
		print "Host ", host, " does not exist in iptables"
	else: # else remove IP rule
		os.system('iptables -D INPUT -s %s -j DROP' % host)
		print "Host ", host, " dropped in iptables"
#####################################################################################
# Function: 	processLastHostOnList(host, count, cutoffTime, limit, totalCount, totalLimit, defaultTime)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	processLastHostOnList(host, count, cutoffTime, limit, totalCount, totalLimit, defaultTime)
#							host		- IP address to look at
#							count		- current count of attempts in timelimit for IP
#							cutoffTime	- time limit for temp bans
#							limit		- number of attempts for temp bans
#							totalCount	- current total attempts for IP
#							totalLimit	- number of attempts for perma bans
#							defaultTime	- ban length
# Returns: 		N/A
# Notes:		
#####################################################################################
def processLastHostOnList(host, count, cutoffTime, limit, totalCount, totalLimit, defaultTime):
	IP = host.split()
	if count >= limit and not timeExpired(int(IP[1]), cutoffTime):
		appendFirewallRule(IP[0])
	else:
		if totalCount > totalLimit:
			appendFirewallRule(IP[0])
		elif timeExpired(int(IP[1]), defaultTime):
			removeFirewallRule(IP[0])
#####################################################################################
# Function: 	Main Driver
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	N/A
# Returns: 		N/A
# Notes:		Parses sorted list, banning/unbanning IPs based on number of failed attempts
#####################################################################################
cutoffTime = setCutOffTime()
defaultTime = setDefaultTime()
limit = setLimit()
count = 0
totalLimit = setTotalLimit()
totalCount = 0

if os.path.getsize(filepath) == 0:
	print "IP_list.txt is empty"
	exit()

with open(filepath, "r") as IP_list:
	prevIP=-1
	
	for currentIP in IP_list:
		cIP = currentIP.split()
		if prevIP!=-1:
			pIP = prevIP.split()
			if cIP[0] != pIP[0]:
				if count >= limit and not timeExpired(int(pIP[1]), cutoffTime):
					appendFirewallRule(pIP[0])
				else:
					print "total count:" , totalCount , " ip: ",pIP[0]
					if totalCount > totalLimit:
						appendFirewallRule(pIP[0])
					elif timeExpired(int(pIP[1]), defaultTime):
						removeFirewallRule(pIP[0])
				
				count = 0
				totalCount = 0
		if not timeExpired(int(cIP[1]), cutoffTime):
			count += 1
		prevIP = currentIP
		totalCount +=1

processLastHostOnList(currentIP, count, cutoffTime, limit, totalCount, totalLimit, defaultTime)
