#!/usr/bin/env python

import socket
import errno
import requests
import getpass
import sys
import telnetlib
import time
from requests.auth import HTTPBasicAuth


def get_file_input_as_list(filePath):
	data = []

	file = open(filePath, "r")

	for line in file:
		data.append(line[:-1])

	file.close()
	return data
