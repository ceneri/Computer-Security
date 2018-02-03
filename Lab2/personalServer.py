#!/usr/bin/env python

import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
import utils
import re
from requests.auth import HTTPBasicAuth

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

PORTS_FILE = "openPorts.txt"
IN_FILE = "skeletonKey.txt"
OUT_FILE = "personalServer.txt"

def get_s_key():
	file = open(IN_FILE, "r")

	for line in file:
		sKey = line[:-1]

	file.close()
	return sKey

def main():

	HOST = IP_ADDRESS

	#Open output file
	file = open(OUT_FILE, "w")

	#Get ports from input file
	openPorts = utils.get_file_input_as_list(PORTS_FILE)

	#Get input Skeleton Key
	skeletonKey = get_s_key()

	#Test every port
	for port in openPorts:

		#Make connection
		tnet = telnetlib.Telnet(HOST, port, timeout=2)
		
		try: 

			#Enter skeletonKey
			tnet.write(skeletonKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			consoleRead = tnet.read_until("Password")

			match = re.search("Pass", consoleRead)

			#Port Found, write to output file
			if match:
				file.write(port + '\n')
				break

			#Try next Port	
			else: 
				continue

		except EOFError, v:

			#Closed connection
			continue

		except:
			continue

	file.close()


if __name__ == '__main__':
	main()