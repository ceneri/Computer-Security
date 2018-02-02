#!/usr/bin/env python

import socket
import errno
import requests
from requests.auth import HTTPBasicAuth

import getpass
import sys
import telnetlib

import time

import skeletonKey as sk

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

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
		#!change to random poort

	#openPorts = []
	file = open(OUT_FILE, "w")

	openPorts = sk.get_ports()

	skeletonKey = get_s_key()

	for port in openPorts:

		print "port", port

		tnet = telnetlib.Telnet(HOST, port)
		
		try: 
			#print skeletonKey
			tnet.write(skeletonKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			consoleRead = tnet.read_until("Password: ", 3)

			if consoleRead == "Password: ":
				portStr = str(port)
				file.write(portStr + '\n')
				break
			else: 
				continue

			#print tnet.read_all()

		except EOFError, v:

			continue
			#print "no"

	file.close()


if __name__ == '__main__':
	main()