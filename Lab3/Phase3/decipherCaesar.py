#!/usr/bin/env python3

#this program is going to decode the decrypted messages
# the results are written to a new file, 
# each file divided by the folder specifying the 
# method that was tried 

# A different program should be used to parse through 
#  those created files and detect which ones contain 
#  only visible characters (and newline)

"""	usage:
		python decipherCaesar.py msg1 [msg ]*
"""
#######################################################
import sys
import os


numOfArgs = len(sys.argv)
destinationDir = "cipherResultsCaesar/"
if not os.path.exists(destinationDir): 
	os.makedirs(destinationDir)
##directory = open( destinationDir+"directory", "w")
#directory.write("Orignal\tOutput")
counter = sys.argv[1]
for x in range(2,numOfArgs):
	#print x	
	try:
		#reading cipher message
		#print "file name is... ", sys.argv[x]
		cipher1FN = sys.argv[x]
		cipher1 = open( cipher1FN, "r")
		#opening output file
		results1 = open( destinationDir+"CaesarResults"+counter+"_"+str(x), "w")#including x in name is for debug purposes
		##directory.write(cipher1FN +"\t"+ destinationDir+"CaesarResults"+str(x)+"\n")
	except:
		print "[Could not open file or file does not exist]"
		continue

	##first message uses rot-13 cipher
	try:
		singleChar = cipher1.read(1)
	except:
		print "This file did not have a single character"
		continue
	while singleChar: #The actual Caesar cipher part
		charAsInt = ord(singleChar)
		if (charAsInt >= 65) and (charAsInt <= 90): #uppercase
			charAsInt-=65
			charAsInt+=13
			charAsInt = charAsInt % 26
			charAsInt+=65
		elif (charAsInt >= 97) and (charAsInt <= 122): #lowercase
			charAsInt-=97
			charAsInt+=13
			charAsInt = charAsInt % 26
			charAsInt+=97
		singleChar= chr(charAsInt)
		results1.write(singleChar)
		singleChar= cipher1.read(1)
	cipher1.close()
	results1.close()
#########################################


#print "finished deciphering"