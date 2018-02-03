#!/usr/bin/env python

import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
from requests.auth import HTTPBasicAuth

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

OUT_FILE = "openPorts.txt"

def main():

	MIN_PORT = 5000
	MAX_PORT = 10000

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

		except socket.error, v:
			errorcode = v[0]
			#if errorcode == errno.ECONNREFUSED:
				#print "Conecction refused"

	file.close()
	

if __name__ == '__main__':
	main()
