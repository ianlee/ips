import linecache
from datetime import datetime
import time
import subprocess, os

filepath = os.path.dirname(os.path.realpath(__file__))+"/IP_list.txt"	

def setCutOffTime():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 1).split()[2]) * 60
def setDefaultTime():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 2).split()[2]) * 60
def setLimit():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 3).split()[2])
def setTotalLimit():
	return int(linecache.getline(os.path.dirname(os.path.realpath(__file__))+"/config.txt", 4).split()[2])

def timeExpired(epoch, cutoffTime):
	return True if(cutoffTime==0 or int(datetime.now().strftime("%s")) - epoch > cutoffTime) else False 

def appendFirewallRule(host):
	notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % host, shell=True, stdout=subprocess.PIPE).communicate()[0]
	if int(notFound): # if IP rule is not already found in iptables, append it
		os.system('logger -p authpriv.notice "*** Blocking SSH attempt from: %s"' % host)
		os.system('iptables -A INPUT -s %s -j DROP' % host)
		print "Host ", host, " added to iptables"
	else:
		print "Host ", host, " already exist in iptables"

def removeFirewallRule(host):
	notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % host, shell=True, stdout=subprocess.PIPE).communicate()[0]
	if int(notFound): # if IP rule does not exist, print message
		print "Host ", host, " does not exist in iptables"
	else: # else drop IP rule
		os.system('iptables -D INPUT -s %s -j DROP' % host)
		print "Host ", host, " dropped in iptables"

def processLastHostOnList(host, count, cutoffTime, limit, totalCount, totalLimit):
	IP = host.split()
	if count >= limit and not timeExpired(int(IP[1]), cutoffTime):
		appendFirewallRule(IP[0])
	else:
		if totalCount > totalLimit:
			appendFirewallRule(IP[0])
		elif timeExpired(int(IP[1]), defaultTime):
			removeFirewallRule(IP[0])

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

processLastHostOnList(currentIP, count, cutoffTime, limit, totalCount, totalLimit)
