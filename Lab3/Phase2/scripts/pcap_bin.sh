#!/bin/bash
#
# File: pcap_bin.sh
#
# Simple shell script that automates server smashing by calling different Python scripts
#
# Usage: $ ./automate.sh [ip address] [skeleton key] [user] [dictionary]
# -----------------------------------------------------------------------------

tshark -r $1 -T fields -e data | tr -d  '\n' > $2