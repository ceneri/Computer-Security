#!/usr/bin/env python3

"""
NSARequests module handles both user and listener interactions with "NSA Supercomputer"

Sources Used:
    https://docs.python.org/2/library/socket.htm
"""

from subprocess import Popen

def callDecryptShell(cipherMessageFile, ivFile, parsedFile, outFolder):

    shProcess = Popen( ["sh", "testMessageDecryption.sh", cipherMessageFile, ivFile, parsedFile, outFolder] )
    # Wait for process to complete.
    shProcess.wait()

