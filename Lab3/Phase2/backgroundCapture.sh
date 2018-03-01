#!/bin/bash

#deleting previous output file
rm nohup.out

#running script in background (it will continue running after you log off)
nohup python -u packetCapt.py &

echo "Periodically check the progress in nohup.out and captpcap/ to make sure it is working correctly"