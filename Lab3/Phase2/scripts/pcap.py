#!/usr/bin/env python3

#tshark -r passwd.pcap -T fields -e data
#tshark -r passwd.pcap -Vx

#say that it uses shell script!!!!!!!!!

#!!!!
#tshark -r ./ceneriPackets/ceneri.key.zip.pcap -T fields -e data | tr -d '\n' > ceneri.zip.data

import sys
import binascii
from subprocess import check_output, Popen

#Shell script location ()
SH_FILE = "./pcap_bin.sh"


def removeIntermediary(intermediaryFile):

    #Call to 'rm'
    iProcess = Popen(["rm", intermediaryFile])
    # Wait for process to complete.
    iProcess.wait()

def writeBinaryToFile(lineStr, outFile):
    file = open(outFile, "wb")
    file.write(binascii.unhexlify(lineStr.rstrip()))  #Strip to avoid trailing newline
    file.close()

def getPCAPData(pcapFile, outputFile):

    #Intermediary file to use as tShark output
    INTERMEDIARY_FILE = "interFile"
    
    #Call to tShark script with output to INTERMEDIARY_FILE
    sh_process = Popen([SH_FILE, pcapFile, INTERMEDIARY_FILE])
    # Wait for process to complete.
    sh_process.wait() 

    #Read contents from INTERMEDIARY_FILE
    inter_contents = open(INTERMEDIARY_FILE,'r').read()

    #Binary to Output file
    writeBinaryToFile(inter_contents, outputFile)

    #Remove intermediary file
    removeIntermediary(INTERMEDIARY_FILE)

def getPasswd(pcapFile, outputFile):

    #Same implementation
    getPCAPData(pcapFile, outputFile)

def getIV(pcapFile, outputFile):

    #Same implementation
    getPCAPData(pcapFile, outputFile)

#https://osqa-ask.wireshark.org/questions/15374/dump-raw-packet-data-field-only
def getZip(pcapFile, outputFile):    

    #Same implementation
    getPCAPData(pcapFile, outputFile)

def getCipherMessage(pcapFile, outputFile):    

    #Same implementation
    getPCAPData(pcapFile, outputFile)

"""
def getPasswd2(pcapFile, outputFile):
    packet_data = check_output(["tshark", "-r", pcapFile, "-T", "fields", "-e", "data"])

    #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string (Second answer)
    data = "".join(map(chr, packet_data))
    data = data[-29:-3]

    writeLineToFile(data, outputFile)
"""




def main():

    #Get file name
    #pcap_file = sys.argv[1]

    #get_passwd(pcap_file)

    #-----------------

    #pcap_file = ("./ceneriPackets/ceneri.key.zip.pcap")
    #ZIP_FILE = "ceneri.zip.data"
    

    #get_zip(pcap_file, ZIP_FILE)

    #------------------

    pcap_file = ("./ceneriPackets/ceneri.passwd.pcap")
    PASS_FILE = "ceneri.passwd"
    

    get_zip(pcap_file, PASS_FILE)


if __name__ == '__main__':
    main()


