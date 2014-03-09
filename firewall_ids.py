import linecache
from datetime import datetime
import time
import subprocess, os

def timeExpired(epoch, cutoffTime):
	return True if(int(datetime.now().strftime("%s")) - epoch > cutoffTime) else False 

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

def processLastHostOnList(host, count, cutoffTime):
	IP = host.split()
	if not timeExpired(int(IP[1]), cutoffTime):
		count += 1
	#print "Last Host: ", IP[0], "Count: ", count
	if count > 4 and not timeExpired(int(IP[0]), cutoffTime):
		appendFirewallRule(IP[0])
	else:
		removeFirewallRule(IP[0])

cutoffTime = 3600 # 60 minutes
count = 0
currentIP = linecache.getline("IP_list.txt", 1)

with open("IP_list.txt", "r") as IP_list:
	nextIP = IP_list.readline()
	
	for nextIP in IP_list:
		cIP = currentIP.split()
		nIP = nextIP.split()
		if cIP[0] != nIP[0]:
			if not timeExpired(int(cIP[1]), cutoffTime):
				count += 1
			#print "Host: ", cIP[0], "Count: ", count
			if count > 4 and not timeExpired(int(cIP[1]), cutoffTime):
				appendFirewallRule(cIP[0])
			else:
				removeFirewallRule(cIP[0])
			cIP = nIP
			count = 0
		if not timeExpired(int(cIP[1]), cutoffTime):
			count += 1
		currentIP = nextIP

processLastHostOnList(currentIP, count, cutoffTime)