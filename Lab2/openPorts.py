#!/usr/bin/env python

import socket
import errno
import requests
from requests.auth import HTTPBasicAuth

import getpass
import sys
import telnetlib

import time

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

def main():

	#take it out of function
	OUT_FILE = "openPorts.txt"

	MIN_PORT = 5000
	MAX_PORT = 10000

	#openPorts = []
	file = open(OUT_FILE, "w")

	for port in range(MIN_PORT, MAX_PORT):

		try:

			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((IP_ADDRESS, port))
			isOpen = clientsocket.send('\n')
			#data = clientsocket.recv(1024)

			if isOpen == 1: 
				portStr = str(port)
				file.write(portStr + '\n')
				#openPorts.append(port)
				#print "port", port

		except socket.error, v:
			errorcode = v[0]
			#if errorcode == errno.ECONNREFUSED:
				#print "Conecction refused"

	file.close()
	

if __name__ == '__main__':
	main()
