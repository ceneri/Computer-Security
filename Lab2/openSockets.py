import socket
import errno
import requests
from requests.auth import HTTPBasicAuth

import getpass
import sys
import telnetlib

import time


"""possible = ['Jean Passepartout', 'JeanPassepartout', 'Jean_Passepartout', 
'jean passepartout', 'jeanpassepartout', 'jean_passepartout',
'jean Passepartout', 'jeanPassepartout', 'jean_Passepartout',
'jean', 'Jean', 'JEAN', 'passepartout', 'Passepartout', 'PASSEPARTOUT',
'JEAN PASSEPARTOUT', 'JEANPASSEPARTOUT', 'JEAN_PASSEPARTOUT',
'Jules Vern', 'JulesVern', 'Jules_Vern', 
'jules vern', 'julesvern', 'jules_vern',
'jules Vern', 'julesVern', 'jules_Vern',
'jules', 'Jules', 'JULES', 'Vern', 'vern', 'VERN',
'JULES VERN', 'JULESVERN', 'JULES_VERN', 'Aouda', 'AOUDA',
'Phileas Fogg', 'PhileasFogg', 'Phileas_Fogg',
'phileas fogg', 'phileasfogg', 'phileas_fogg',
'phileas Fogg', 'phileasFogg', 'phileas_fogg',
'phileas', 'Phileas', 'PHILEAS', 'Fogg', 'fogg', 'FOGG',
'PHILEAS FOGG', 'PHILEASFOGG', 'PHILEAS_FOGG',
'Reform Club', 'ReformClub', 'Reform_Club'
'reform club', 'reformclub', 'reform_club',
'reform Club', 'reformClub', 'reform_Club',
'reform', 'Reform', 'REFORM', 'Club', 'CLUB', 'club',
'REFORM CLUB', 'REFORMCLUB', 'REFORM_CLUB',
'Goes Everywhere', 'GoesEverywhere', 'Goes_Everywhere',
'goes everywhere', 'goeseverywhere', 'goes_everywhere', 
'goes Everywhere', 'goesEverywhere', 'goes_Everywhere'
'GOES EVERYWHERE', 'GOESEVERYWHERE', 'GOES_EVERYWHERE'
'PASSPORT', 'passport', 'Passport', 
'passe-partout', 'PASSE-PARTOUT', 'passe_partout', 'PASSE_PARTOUT',
]"""

possible = ['JeanPassepartout', 'Jean_Passepartout', 'Jean-Passepartout',
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

IP_ADDRESS = '128.114.59.215'
URL = 'http://128.114.59.215:'
UNAME = 'ceneri'
PWRD = ''

openPorts = []

for i in range(5000, 10001):

	try:
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((IP_ADDRESS, i))
		isOpen = clientsocket.send('\n')
		#data = clientsocket.recv(1024)
		#print "data", repr( data ), i 

		if isOpen == 1 or isOpen == "1":
			print "port", i
			openPorts.append(i)

	except socket.error, v:
		errorcode = v[0]
		#if errorcode == errno.ECONNREFUSED:
			#print "Conecction refused"
	

	#if isOpen == "1":
	#	print "Open port:", i


print "Total number of sockets is", len(openPorts)
print openPorts

#***********

"""for port in openPorts:

	port_str = str(port)

	for skeleton in possible:
		PWRD = skeleton

		
		#response = requests.get(URL + port_str + "/" + skeleton, auth=HTTPBasicAuth(UNAME, ''))
		response = requests.get(URL + port_str + "/" + skeleton)

		#if response.status_code == 201 or response.status_code == 202:
		if response.status_code != 404:
			print "Port", port, "response", response
"""
 #requests.get('http://128.114.59.215:5028', auth=HTTPBasicAuth('ceneri',''))

print "telnet"

#for sKey in possible:
#https://docs.python.org/2.4/lib/telnet-example.html

sKey = 'passepartout'

HOST = IP_ADDRESS
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()

tn = telnetlib.Telnet(HOST, str(openPorts[0]))


#tn.write("GET /" + sKey + " HTTP/1.0")
print sKey
tn.write(sKey + "\n")
#print "GET /" + sKey + " HTTP/1.0"
#print tn.read_all()

tn.read_until("Username: ")
tn.write(UNAME + "\n")
print tn.read_all()

time.sleep(.1) 
