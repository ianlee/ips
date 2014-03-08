import time
import re

for line in open("/var/log/secure"):
	if "Failed password for" in line:
		tokens = re.split('  | |\n', line)
		date_str = ' '.join(tokens[0:3])
		date_format = date_str + " 2014"
		the_date = str(int(time.mktime(time.strptime(date_format,'%b %d %H:%M:%S %Y'))))
		list_of_clients = tokens[10] + ' ' + the_date
		print list_of_clients
