#!/usr/bin/env python3

#this program is going to decode the decrypted messages
# the results are written to a new file, 
# each file divided by the folder specifying the 
# method that was tried 

# A different program should be used to parse through 
#  those created files and detect which ones contain 
#  only visible characters (and newline)

"""	usage:
		python decipherChainRot.py msg1 [msg ]*
"""
#######################################################
import sys
import os


numOfArgs = len(sys.argv)
destinationDir = "cipherResultsChainRot/"
if not os.path.exists(destinationDir): 
	os.makedirs(destinationDir)
rotNums = [20,19,18,17] #opposite of the rotation pattern that was [7,8,9,6]
counter = sys.argv[1]
for x in range(2,numOfArgs):
	index=0
	try:
		#reading cipher message
		#print "file name is... ", sys.argv[x]
		cipher1FN = sys.argv[x]
		cipher1 = open( cipher1FN, "r")
		#opening output file
		results1 = open( destinationDir+"ChainRot"+counter+"_"+str(x), "w")#including x in name is for debug purposes
	except:
		print "[Could not open file or file does not exist]"
		continue

	
	try:
		singleChar = cipher1.read(1)
	except:
		print "This file did not have a single character"
		continue
	while singleChar: #The actual ChainRot cipher part
		charAsInt = ord(singleChar)
		if (charAsInt >= 65) and (charAsInt <= 90): #uppercase
			charAsInt-=65
			charAsInt+=rotNums[index]
			charAsInt = charAsInt % 26
			charAsInt+=65
		elif (charAsInt >= 97) and (charAsInt <= 122): #lowercase
			charAsInt-=97
			charAsInt+=rotNums[index]
			charAsInt = charAsInt % 26
			charAsInt+=97
		singleChar= chr(charAsInt)
		results1.write(singleChar)
		#print singleChar," (", ord(singleChar),") obtained with rotNum by ",rotNums[index] 
		singleChar= cipher1.read(1)
		#if (charAsInt >= 32 ) or (singleChar == "\n") or (singleChar == "\r\n"):
		index = (index+1)%4
	cipher1.close()
	results1.close()
#########################################


#print "finished deciphering"

