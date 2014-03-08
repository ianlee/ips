import time
from datetime import datetime
import re
import os

def parseDate(line):
	tokens = re.split('  | |\n', line)
	date_format = ' '.join(tokens[0:3]) + " " + str(datetime.now().year)
	the_date = str(int(time.mktime(time.strptime(date_format,'%b %d %H:%M:%S %Y'))))
	return the_date


def parseIP(line):
	tokens = re.split('  | |\n', line)
	return tokens[10]

IP_list = open("IP_list.txt", "w")

with open("/var/log/secure") as fsecure:
	for line in fsecure:
		if "sshd" and "Failed password for" in line:
			date = parseDate(line)
			IP = parseIP(line)
			print IP, date
			IP_list.write(IP + " " + date + "\n")

IP_list.close()

#os.system("sh scan_secure.sh")
