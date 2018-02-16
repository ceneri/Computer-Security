#!/usr/bin/env python

import socket
from personalServer import get_s_key
from dictionaryPasswd import get_p_port


UNAME = 'ceneri'
IP_ADDRESS = '128.114.59.215'

IN_FILE = "dictionaryPasswd.txt"

def get_passwd():
    file = open(IN_FILE, "r")

    for line in file:
        passwd = line[:-1]

    file.close()
    return passwd

#https://pythongeekstuff.wordpress.com/2015/07/29/file-transfer-server-using-socket/
def download_file(filename, address, port, skey, passwd):

    #remove file extension
    command = filename.split(".")[0]
    print command

    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockt.connect((address, port ))

    sData = "Temp"
     
    while True:
        sockt.send(skey)
        sData = sockt.recv(1024)
        sockt.send(UNAME)
        sData = sockt.recv(1024)
        sockt.send(passwd)
        sData = sockt.recv(1024)
        sockt.send(command)
        fDownloadFile = open(filename,"wb")
        while sData:
            sData = sockt.recv(1024)
            fDownloadFile.write(sData)            
        print "Download Completed"
        break
     
    sockt.close()
    fDownloadFile.close()



def main():

    pPort = int(get_p_port())
    sKey = get_s_key()
    passwd = get_passwd()

    binary = "binary.bin"
    source = "source.c"
    #.cnf, .conf, .cfg, .cf or as well .ini
    config = "config"


    #
    download_file(binary, IP_ADDRESS, pPort, sKey, passwd)
    download_file(source, IP_ADDRESS, pPort, sKey, passwd)
    download_file(config, IP_ADDRESS, pPort, sKey, passwd)

    

if __name__ == '__main__':
    main()

