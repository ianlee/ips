import time
from datetime import datetime
import re
from operator import itemgetter
import os

def parseDate(line):
	tokens = re.split('  | |\n', line)
	dateFormat = ' '.join(tokens[0:3]) + " " + str(datetime.now().year)
	epochDate = str(int(time.mktime(time.strptime(dateFormat,'%b %d %H:%M:%S %Y'))))
	return epochDate


def parseIP(line):
	tokens = re.split('  | |\n', line)
	return tokens[10]

def writeListToFile(IPlist):
	with open(os.path.dirname(os.path.realpath(__file__))+'/IP_list.txt', 'w') as fList:
		for el in IPlist:
			fList.write('{0}\n'.format(' '.join(el)))

IPlist = []
print os.path.dirname(os.path.realpath(__file__))
with open("/var/log/secure") as fsecure:
	for line in fsecure:
		if "sshd" and "Failed password for" in line:
			epochDate = parseDate(line)
			IP = parseIP(line)
			print IP, epochDate
			IPlist.append([IP,epochDate])

IPlist.sort(key=itemgetter(0,1))
writeListToFile(IPlist)
#print IPlist
execfile(os.path.dirname(os.path.realpath(__file__))+"/firewall_ids.py" )
