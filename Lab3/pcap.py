#!/usr/bin/env python3

#tshark -r passwd.pcap -T fields -e data
#tshark -r passwd.pcap -Vx

#!!!!
#tshark -r ./ceneriPackets/ceneri.key.zip.pcap -T fields -e data | tr -d '\n' > ceneri.zip.data

import sys
import binascii
from subprocess import check_output, Popen

def get_passwd(pcap_file):
    packet_data = check_output(["tshark", "-r", pcap_file, "-T", "fields", "-e", "data"])

    #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string (Second answer)
    data = "".join(map(chr, packet_data))
    data = data[-29:-3]
    print(data)


#https://osqa-ask.wireshark.org/questions/15374/dump-raw-packet-data-field-only
def get_zip(pcap_file, zip_file):

    SH_FILE = "./pcap_bin.sh"
    

    sh_process = Popen([SH_FILE, pcap_file, zip_file])
    sh_process.wait() # Wait for process to complete.

    # iterate on the stdout line by line
    #for line in process.stdout.readlines():
        #print(line)
    
    zip_contents = open(zip_file,'r').read()

    #Open output files
    OUT_FILE =  "key.zip"
    file = open(OUT_FILE, "wb")
    file.write(binascii.unhexlify(zip_contents.rstrip()))  #Strip to avoid trailing newline
    file.close()

    #sys.stdout.write(binascii.unhexlify(zip_contents)) # needs to be stdout.write to avoid trailing newline

def get_pa(pcap_file, passwd_file):

    SH_FILE = "./pcap_bin.sh"
    
    sh_process = Popen([SH_FILE, pcap_file, passwd_file])
    sh_process.wait() # Wait for process to complete.

    # iterate on the stdout line by line
    #for line in process.stdout.readlines():
        #print(line)
    
    zip_contents = open(passwd_file,'r').read()

    #Open output files
    OUT_FILE =  "password.txt"
    file = open(OUT_FILE, "wb")
    file.write(binascii.unhexlify(zip_contents.rstrip()))  #Strip to avoid trailing newline
    file.close()

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


