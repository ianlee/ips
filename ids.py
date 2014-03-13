import time
from datetime import datetime
import re
from operator import itemgetter
import os
#####################################################################################
# Function: 	parseDate (line)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	parseDate (line)
# 							line - line from log file to parse date from
# Returns: 		string - epoch date from line
# Notes:
#####################################################################################
def parseDate(line):
	tokens = re.split('  | |\n', line)
	dateFormat = ' '.join(tokens[0:3]) + " " + str(datetime.now().year)
	epochDate = str(int(time.mktime(time.strptime(dateFormat,'%b %d %H:%M:%S %Y'))))
	return epochDate

#####################################################################################
# Function: 	parseIP (line)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	parseIP (line)
# 							line - line from log file to parse IP from
# Returns: 		string - IP address from line
# Notes:
#####################################################################################
def parseIP(line):
	tokens = re.split('  | |\n', line)
	return tokens[10]
#####################################################################################
# Function: 	writeListToFile(IPlist)
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	writeListToFile(IPlist)
# 							IPlist - list of IP's and their epoch dates
# Returns: 		N/A
# Notes:
#####################################################################################
def writeListToFile(IPlist):
	with open(os.path.dirname(os.path.realpath(__file__))+'/IP_list.txt', 'w') as fList:
		for el in IPlist:
			fList.write('{0}\n'.format(' '.join(el)))

#####################################################################################
# Function: 	Main Driver
# Date: 		2014/3/11
# Revisions:
# Designer:		Ian Lee & Luke Tao
# Programmer:	Ian Lee & Luke Tao
# Interface: 	N/A
# Returns: 		N/A
# Notes:		Parses the /var/log/secure file, saves parsed data, then executes firewall_ids.py
#####################################################################################
IPlist = []
print os.path.dirname(os.path.realpath(__file__))
with open("/var/log/secure") as fsecure:
	for line in fsecure:
		if "sshd" and "Failed password for" in line:
			# get data from each line
			epochDate = parseDate(line)
			IP = parseIP(line)
			print IP, epochDate
			IPlist.append([IP,epochDate])
#sort list
IPlist.sort(key=itemgetter(0,1))
#write list to file
writeListToFile(IPlist)
#run next step in process
execfile(os.path.dirname(os.path.realpath(__file__))+"/firewall_ids.py" )
