import re

with open("IP_list.txt", "r") as IP_list:
	data = IP_list.readlines()

	for line in data:
		IP_and_time = re.split(' |\n', line)
		print IP_and_time