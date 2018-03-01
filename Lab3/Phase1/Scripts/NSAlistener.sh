#!/bin/bash

#port# must be >=4000
startPort=54545

#mkfifo testFifo

#while read encryptedPass
#do
#may need -k
nc  -l $1 $2 > $3

#done < passwd.crypt

echo DONE
