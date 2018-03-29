#!/usr/bin/env python3

"""
kyParser takes as input file containing an obfuscated key (Long string of characters)
and outputs all possible substrings of size KEY_SIZE to a line in the specified output file

To call script:

	python  keyParser.py <inputFileName> <outputFileName>

"""

import sys

#Const Values
KEY_SIZE = 32

def getObfuscatedKey(key_file):
	file = open(key_file, "r")

	for line in file:
		key = line[:-1]

	file.close()
	return key

def keyParsing(input_file, output_file):

	#Get obfuscated key
	obfuscated =getObfuscatedKey(input_file)
	obfLength = len(obfuscated)

	#Open File for writing
	file = open(output_file, "w")

	for i in range(obfLength - KEY_SIZE + 1):
		file.write(obfuscated[i:i+32] + '\n')

	file.close()


def main():

	#Get file arguments 
	INPUT_FILE = sys.argv[1]
	OUTPUT_FILE = sys.argv[2]

	keyParsing(INPUT_FILE, OUTPUT_FILE)



if __name__ == '__main__':
	main()