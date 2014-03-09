import linecache
from datetime import datetime
import time
import subprocess, os

def timeExpired(epoch, cutoffTime):
	return True if((int(datetime.now().strftime("%s")) - epoch > cutoffTime)) else False 

cutoffTime = 1800 # 30 minutes
count = 0
currentIP = linecache.getline("IP_list.txt", 1)

with open("IP_list.txt", "r") as IP_list:
	nextIP = IP_list.readline()
	
	for nextIP in IP_list:
		cIP = currentIP.split()
		nIP = nextIP.split()
		
		if cIP[0] != nIP[0]:
			count += 1
			if count > 4:
				notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % cIP[0], shell=True, stdout=subprocess.PIPE).communicate()[0]
				if int(notFound): # if IP rule is not already found in iptables, append it
					os.system('logger -p authpriv.notice "*** Blocking SSH attempt from: %s"' % cIP[0])
					os.system('iptables -A INPUT -s %s -j DROP' % cIP[0])
					print "Host ", cIP[0], " added to iptables"
				else:
					print "Host ", cIP[0], " already exist in iptables"
			else:
				notFound = subprocess.Popen("iptables-save | grep -q %s; echo $?" % cIP[0], shell=True, stdout=subprocess.PIPE).communicate()[0]
				if int(notFound):
					print "Host ", cIP[0], " does not exist in iptables"
				else:
					os.system('iptables -D INPUT -s %s -j DROP' % cIP[0])
					print "Host ", cIP[0], " dropped in iptables"
				# Will find a way to check if the IP rule doesn't exist
				# //potentially can check vs different cutoff time for removal of block time
				#//check vs current line's time stamp
				

			count = 0
			currentIP = nextIP
		if not timeExpired(int(cIP[1]), cutoffTime):
			count += 1

		currentIP = nextIP