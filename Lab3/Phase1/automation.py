#!/usr/bin/env python3

"""
Script usage:

    python automation.py <username> <passwdPCAPFile> <IVPCAPFile> <keyPCAPFile> <msgPCAPFile>
"""


import sys
import pcap
import unzip
import keyParser
import NSARequests as nsa
import multiprocessing as mp

#Constant values
PASWWD_FILE = "passwd"
IV_FILE = "iv"
KEY_FILE = "key.zip"
MESSAGE_FILE = "cipherMessage"

PASSWORD_PLAIN = "password.plain"
KEY_PLAIN = "key"

KEY_PARSED = "key.parsed"

#Const values
NSA_HOST = '128.114.59.42'
NSA_PORT = 2001
LOCAL_HOST = '128.114.59.29 '
LOCAL_PORT = 54545 


def main():

    #-------------------------------USER INPUT-------------------------

    #User input should be the username followed by 4 PCAP files
    USERNAME = sys.argv[1] + '_'
    PASWWD_PCAP = sys.argv[2]
    IV_PCAP = sys.argv[3]
    KEY_PCAP = sys.argv[4]
    MESSAGE_PCAP = sys.argv[5]

    #--------------------------PCAP -> DATA FILES ----------------------------

    #username specific file names
    passwd_file = USERNAME + PASWWD_FILE
    iv_file = USERNAME + IV_FILE
    key_file = USERNAME + KEY_FILE
    message_file = USERNAME + MESSAGE_FILE

    #Generate data files from PCAP files
    pcap.getPasswd( PASWWD_PCAP, passwd_file)
    pcap.getIV( IV_PCAP, iv_file)
    pcap.getZip( KEY_PCAP, key_file)
    pcap.getCipherMessage( MESSAGE_PCAP, message_file)

    #----------------------------NSA Request--------------------------------

    #Obtain encrypted password
    cryptFile = open(passwd_file, "r")
    cryptedPass=cryptFile.readline().strip()+' '

    #!!!Later on change port to be random and check if its used
    #Send request in a child process
    userProcess = mp.Process(target=nsa.NSA_user, args=((LOCAL_HOST, LOCAL_PORT, cryptedPass)) )
    userProcess.start()

    #Listener
    passwd_plain = USERNAME + PASSWORD_PLAIN
    nsa.NSA_listener('', LOCAL_PORT, passwd_plain)

    #Join child process
    userProcess.join() 


    #--------------------------Unzip Key----------------------------

    #Obtain password
    pFile = open(passwd_plain, "r")
    password = pFile.read()
    pFile.close()

    #Get the second part
    password = password.split(" ")
    password = password[1]
    password = password[:-1]
    
    print password

    #Unzip and create key file
    key_plain = USERNAME + KEY_PLAIN
    unzip.unzipFile(key_file, key_plain, password)


    #--------------------------Parse Key----------------------------

    key_parsed = USERNAME + KEY_PARSED
    keyParser.keyParsing(key_plain, key_parsed)



if __name__ == '__main__':
    main()