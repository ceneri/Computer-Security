#!/usr/bin/env python3

"""
NSARequests module handles both user and listener interactions with "NSA Supercomputer"

Sources Used:
    https://docs.python.org/2/library/socket.html
"""

import sys
import time
import socket
import multiprocessing as mp
from subprocess import check_output


#Const values
NSA_HOST = '128.114.59.42'
NSA_PORT = 2001
LOCAL_HOST = '128.114.59.29 '
LOCAL_PORT = 54545

INPUT_FILE = "passwd.crypt"
OUTPUT_FILE = "listenerOutput" 



def NSA_user(localhost, lport, crypt_passwds):
    """Method implements the following command using python:
            echo $encrpytedPass 128.114.59.29 $portNum | nc 128.114.59.42 2001
    """

    #Sleep to allow listener method to begin
    time.sleep(3)

    #Send a request for each password passed 
    for cPasswd in crypt_passwds:

        #Create socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect( (NSA_HOST, NSA_PORT) )

        message = cPasswd + localhost + str(lport)
        s.sendall(message)
        print ("Sending request: " + message)

        #Print response (OK/BUSY)
        response = s.recv(1024)
        print ("Response Code: " + response)

        s.close()

def NSA_listener(localhost, lport, outfile, numRequests):
    """Method tries to implement the following command using python:
            nc -l 128.114.59.29 55543 >> listenerOutput
    """
    received = 0

    #Start timer
    start = time.time()

    #Open output file
    outFile = open(outfile, "w")

    #Socket bind to local port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((localhost, lport))

    #Listen
    print("Listening...")
    s.listen(1)

    while received < numRequests:

        conn, addr = s.accept()
        print ('Connected by '+ str(addr)) 

        #Write data received
        while 1:
            data = conn.recv(1024)
            if not data: break
            outFile.write(data)
            print data

        received += 1

    print ("Done")
    s.close()
    outFile.close()
    
    #Stop and print timer
    end = time.time()
    print("Listening time: " + str(end - start) + " seconds")


def main():
    """Main sends request and listents for "NSA Response" 
    Arguments:
        1 - Input File      (Optional)
        2 - Output File     (Optional)
        3 - Local Host      (Optional)
        4 - Local Port      (Optional)

    Sample call:

        python passwd.crypt listenerOutput 128.114.59.29 54545
    """

    #Obtain optional arguments
    """args = sys.argv
    inputFile = args[1] if len(args) > 1 else INPUT_FILE
    outputFile = args[2] if len(args) > 2 else OUTPUT_FILE
    localHost = args[3]+' ' if len(args) > 3 else LOCAL_HOST
    localPort = int(args[4]) if len(args) > 4 else LOCAL_PORT

    #Obtain encrypted password
    cryptFile = open(inputFile, "r")
    cryptedPass=cryptFile.readline().strip()+' '

    #Send request in a child process
    userProcess = mp.Process(target=NSA_user, args=((localHost, localPort, cryptedPass)) )
    userProcess.start()"""

    #Listener
    NSA_listener('', 52696, "lol", 2)

    #Join child process
    #userProcess.join() 


if __name__ == '__main__':
    main()