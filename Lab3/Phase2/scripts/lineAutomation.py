#!/usr/bin/env python3

"""
Script usage:

    python lineAutomation.py 
"""

from subprocess import Popen

def callLineAutomateShell(username, passwdPCAPFile, IVPCAPFile, keyPCAPFile, msgPCAPFile):

    shProcess = Popen( ["sh", "lineAutomation.sh", username, passwdPCAPFile, IVPCAPFile, keyPCAPFile, msgPCAPFile] )
    # Wait for process to complete.
    shProcess.wait()


def lineAutomation():

    useNameCounter = 0
    pcapNaming = "pcapData"

    for i in range(51, 2610, 32):
        passwdPcap = pcapNaming + str(i) + '.pcap'
        keyzipPcap = pcapNaming + str(i + 8) + '.pcap'
        ivPcap = pcapNaming + str(i + 16) + '.pcap'
        msgPcap = pcapNaming + str(i + 24) + '.pcap'

        username = "user" + str(useNameCounter)
        useNameCounter += 1

        callLineAutomateShell(username, passwdPcap, ivPcap, keyzipPcap, msgPcap)


def main():

    lineAutomation()


if __name__ == '__main__':
    main()