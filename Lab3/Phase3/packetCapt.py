#!/usr/bin/env python3

#this program tries to capture packets using a socket

"""Sources Used:
    https://docs.python.org/2/library/socket.html
"""

###TODO### (last updated 3/6)
# Filter out pcaps that don't have a payload with at least one byte 
# Optimize code
# Use multiple threads to guarantee we get every packet

### How to test ### (last updated 2/28)
# On one terminal, run ./backgroundCapture.sh
# On a different terminal, run this: 
#   while true; do nc 128.114.59.42 5001 | tshark -i - 2>/dev/null; done
# The second terminal shows the pcaps that this program is trying to capture

### Current bugs ### (last updated 2/25)
# captures more pcaps than are being sent (maybe they are duplicate pcaps?)

import socket
import sys
import os
import time

"""Setting up the socket"""
HOST='128.114.59.42'
PORT=5001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

"""Setting up output files"""
#https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
packetCaptNumber=2	 ##TODO change this so that we could maybe have this set by user input
if not os.path.exists("captpcap"+str(packetCaptNumber)): 
    os.makedirs("captpcap"+str(packetCaptNumber))

fileName="captpcap"+str(packetCaptNumber)+"/pcapData"
fileEnding=".pcap"
fileNo=0

#######debug stuff 
startTime = time.localtime(time.time()) ##for debugging
print "Local current start time :", startTime


##variables to control the time period in which we capture packets
startH=1
stopH=2

startM=57
stopM=15



localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "This program was started at ",currHour,":",currMin


print"waiting for right time"
if not(((currHour==startH) and (currMin >= startM)) or ((currHour==stopH) and (currMin < stopM))) : 
	localtime = time.localtime(time.time())
	currHour=localtime.tm_hour
	currMin=localtime.tm_min
	if currMin < startM:
		sleepTimeM=(startM-currMin)*60
		print "Sleeping for ", startM-currMin, " minutes..." 
		time.sleep(sleepTimeM) #sleep until the 57th of the hour
	if currHour==0: ###if debugging, comment this line and the rest of this if statement
		time.sleep(1*60*60) #sleep for one hour
		print "Sleeping for one hour..."
	elif currHour > startH:
		sleepTimeH=(25-currHour)*3600 #3600=60*60
		print "Sleeping for ", 25-currHour, " hours..."
		time.sleep(sleepTimeH)
		#############

"""Continuous loop of pcap capturing"""
print "Entering capture loop"
localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Stopped waiting at ",currHour,":",currMin
while ((currMin >= (startM-1)) or (currMin < stopM) ):#(((currHour==AMstartH) and (currMin >= startM)) or ((currHour==AMstopH) and (currMin <= stopM))) : 
    try:
        localtime = time.localtime(time.time())
        currHour=localtime.tm_hour
        currMin=localtime.tm_min
        print "Local current time :", localtime
        print "[fileNo=", fileNo, "] [currMin=", currMin,"] [currHour=", currHour,"]"
        #print "ClockTime is ", localtime.tm_hour,":",localtime.tm_min
        pcapOut = open( fileName+str(fileNo)+fileEnding, 'w')
        pcapData=s.recv(4096)
        #print pcapData #debug
        pcapOut.write(pcapData)
        pcapOut.close()
        fileNo+= 1
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
        try:
        	s.connect((HOST,PORT))
    	except:
    		print "It wasn't a connection error"
"""Program End"""
localtime = time.localtime(time.time())
currHour=localtime.tm_hour
currMin=localtime.tm_min
print "Finished capturing at ",currHour,":",currMin
print "done"
s.close()
