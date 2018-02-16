#!/bin/bash
# File: automate.sh
# Author: Cesar Neri <ceneri@ucsc.edu>
# Date Created: February 16, 2018
#
# Simple shell script that automates server smashing by calling different Python scripts
#
# Usage: $ ./automate.sh [ip address] [skeleton key] [user] [dictionary]
# -----------------------------------------------------------------------------

python openPorts.py
