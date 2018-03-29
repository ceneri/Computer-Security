#!/usr/bin/env python3

"""
Script usage:

	python <username> <passwdPCAPFile> <IVPCAPFile> <keyPCAPFile> <msgPCAPFile>
"""


import sys
import pcap

#Constant values
PASWWD_FILE = "passwd"
IV_FILE = "iv"
KEY_FILE = "key.zip"
MESSAGE_FILE = "cipherMessage" 


def main():

	#Later pcap files should be input
	USERNAME = sys.argv[1] + '_'
	PASWWD_PCAP = sys.argv[2]
	IV_PCAP = sys.argv[3]
	KEY_PCAP = sys.argv[4]
	MESSAGE_PCAP = sys.argv[5]

	#Create password file
	pcap.getPasswd( PASWWD_PCAP, USERNAME + PASWWD_FILE)

	#Create IV file
	pcap.getIV( IV_PCAP, USERNAME + IV_FILE)

	#Create IV file
	pcap.getZip( KEY_PCAP, USERNAME + KEY_FILE)

	#Create IV file
	pcap.getCipherMessage( MESSAGE_PCAP, USERNAME + MESSAGE_FILE)




if __name__ == '__main__':
	main()