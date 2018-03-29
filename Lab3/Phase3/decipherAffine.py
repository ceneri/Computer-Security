#!/usr/bin/env python3

#this program is going to decode the decrypted messages
# the results are written to a new file, 
# each file divided by the folder specifying the 
# method that was tried 

# A different program should be used to parse through 
#  those created files and detect which ones contain 
#  only visible characters (and newline)

"""	usage:
		python decipherAffine.py msg1 [msg ]*
"""
#######################################################
import sys
import os


numOfArgs = len(sys.argv)
destinationDir = "cipherResultsAffine/"
if not os.path.exists(destinationDir): 
	os.makedirs(destinationDir)
counter = sys.argv[1]
#hardcoding the dictionary because it doesn't seem to be changed
affineDict={'11':'a', '12':'b', '13':'c', '14':'d', '15':'e',
			'21':'f', '22':'g', '23':'h', '24':'i', '25':'j',
			'31':'k', '32':'l', '33':'m', '34':'n', '35':'o',
			'41':'p', '42':'q', '43':'r', '44':'s', '45':'t',
			'51':'u', '52':'v', '53':'w', '54':'x', '55':'y'}


for x in range(2,numOfArgs):
	try:
		#reading cipher message
		#print "file name is... ", sys.argv[x]
		cipher1FN = sys.argv[x]
		cipher1 = open( cipher1FN, "r")
		#opening output file
		#including x in name is for debug purposes
		results1 = open( destinationDir+"Affine"+counter+"_"+str(x), "w")
	except:
		print "[Could not open file or file does not exist]"
		continue

	try:
		firstChar = cipher1.read(1)
	except:
		print "This file did not have a single character"
		continue
	while firstChar: #The actual Affine cipher part
		charAsInt = ord(firstChar)
		if (firstChar == ' '): #converting double spaces to single
			secondChar = cipher1.read(1)
			if (secondChar == ' '):
				results1.write(firstChar)
		elif (charAsInt >= 48) and (charAsInt<=57): #int range
			secondChar = cipher1.read(1)
			char2AsInt = ord(secondChar)
			#print firstChar
			if (char2AsInt >= 48) and (char2AsInt<=57): #if second is also int
				#combine into a single number
				#and then use dictionary to write appropriate letter
				#print secondChar
				#results1.write(firstChar)
				#results1.write(secondChar)
				combinedChars = firstChar + secondChar
				charsAsInt = int(combinedChars)
				#print combinedChars, "as int --> ",charsAsInt
				#print charAsInt
				results1.write(affineDict[combinedChars])
			else: #proceed as if nothing happened if 2nd char not a number
				#There might be a bug here that might be fixed by moving the file pointer
				results1.write(firstChar)
				results1.write(secondChar)
		else:
			results1.write(firstChar)
		firstChar= cipher1.read(1)
	cipher1.close()
	results1.close()
#########################################


#print "finished deciphering"