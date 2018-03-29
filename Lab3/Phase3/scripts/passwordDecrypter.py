#!/usr/bin/env python3

"""
Script usage:
"""

import sys
import pcap
import unzip
import NSARequests as nsa
import multiprocessing as mp

#Const values
NSA_HOST = '128.114.59.42'
NSA_PORT = 2001
LOCAL_HOST = '128.114.59.29 '
LOCAL_PORT = 52696

def passwdOnlyFile(inputFile, outputFile):

    #Get file contents to a list
    with open(inputFile) as f:
        content = f.readlines()

    pFile = open(outputFile, "w")

    for line in content:
        pFile.write(line.split(" ")[1])

    pFile.close
    

def requests(cPasswds, outputFile):
    """Prints all responses to arbitrary outputFile"""

    """cPasswds = []

    for pfile in passwd_files:
        #Obtain encrypted password
        cryptFile = open(pfile, "r")
        cryptedPass=cryptFile.readline().strip()+' '

        cPasswds.append(cryptedPass)"""

    #!!!Later on change port to be random and check if its used
    #Send request in a child process
    userProcess = mp.Process(target=nsa.NSA_user, args=((LOCAL_HOST, LOCAL_PORT, cPasswds)) )
    userProcess.start()

    #Listener
    nsa.NSA_listener('', LOCAL_PORT, outputFile, len(cPasswds) )

    #Join child process
    userProcess.join() 

def main():

    #cryptPs = ['epZ3maUPg.5bM', 'toDomUXturxgE', 'arjTn5JkJn1eQ', 'pa9dUC4SyB.Ok', 'sswsoxTKa60Ck', 'areI1u8PUKnCE', 'arEuwZJu/coYM', 'itTr4l7DBqOTg', 'pa8f6N7v.ZWtE', 'sso2.6YcMAD36',
        #'itDjFKQjy2AoA', 'ssa8iK1EEkU7Q', 'sssSFzvWQNGbM', 'ss1BZQcb/ZlTs', 'top4SXdRhypNg', 'epEkR5mNJ.KN6', 'pajwdHh82DFAA', 'epA6qvwC.NxW.', 'pa51cvzXQFikI', 'epWP3sY5xFY/c']

    cryptPs, packetNames, outNames = [],[],[]
    pname = "../captpcap1/pcapData"
    n = 0

    for i in range(101):
        j = i + n
        packetNames.append(pname + str(j) + '.pcap')
        outNames.append(packetNames[i] + '.out')

        pcap.getPasswd( packetNames[i], outNames[i])

        #Obtain encrypted password
        cryptFile = open(outNames[i], "r")
        cryptedPass = cryptFile.readline().strip()+' '

        cryptPs.append(cryptedPass)


    PASS_OUTPUTFILE = "../dPasswrods0"
    #inFile = "../captpcap1/" + sys.argv[1]
    #outFile = "passwordsOUT"
    #pcap.getPasswd( inFile, outFile)

    

    #----------------------------NSA Request--------------------------------

    requests(cryptPs, PASS_OUTPUTFILE)

    #----------------------------Write passwords to files--------------------------------
    
    """"passwd_plains = []
    
    #Get file contents to a list
    with open(PASS_OUTPUTFILE) as f:
        content = f.readlines()

    passwds = []

    for i in range(numberOfUsers):

        #obtain password
        p = content[i].strip()
        p = p.split(" ")[1]
        passwds.append(p)

        #create plain password file path
        passwd_plains.append(OUT_FOLDERS[i] + USERNAMES[i] + PASSWORD_PLAIN)

        #write password plain file
        pFile = open(passwd_plains[i], "w")
        pFile.write(passwds[i] + '\n')
        pFile.close"""


if __name__ == '__main__':
    main()