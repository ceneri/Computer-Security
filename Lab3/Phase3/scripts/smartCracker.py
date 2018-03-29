#!/usr/bin/env python3

import time
import crypt
from sets import Set

def getSalt(password):
    return password[0:2]

def sortPasswds(filename):

    passwds = []
    
    with open(filename, 'r') as f:
        passwds = f.readlines()
        
    passwds.sort()
    print "sorted"

    with open(filename, 'w') as f:

        for passwd in passwds:
            f.write( passwd.strip('/n') )

def getAllSubstrs(filename):

    substrs = Set()
    passwds = []
    
    with open(filename, 'r') as f:
        passwds = f.readlines()
        
    for passwd in passwds:
        substrs.add(passwd[:2])
        substrs.add(passwd[2:4])
        substrs.add(passwd[4:0])

    print "Number of substrings:", len (substrs)
    print "Substrings:\n", ', '.join(substrs)

def crack(cryptPasswd):
    """Returns string password cracked"""

    salt = getSalt(cryptPasswd)

    substrings = ['Ni', '9k', 'zo', 'BB', 'va', 'Ea', 'tI', 'Om', 'ec', 'Pb', 'FC', 'gc', 'Ls', 'd9', 'Tf', '3B', 'RW', 'us', 'xC', 
                    '7L', 'je', 'Da', 'pb', 'lt', 'Wt', 'ip', '5a', 'Ja', 'Yw', 'nw', 'b3', 'Hf', 'Ma', 'qT', 'yH', 'fy', 'Km', 'St',
                    'a0', 'Ch', 'Ui', 'hC', 'sC', 'Qh', '8p', 'oS', 'c6', '0s', '2w', 'Gs', 'wA', 'kd', 'Xc', 'mi', 'Zb', 'rh', 'Va', 
                    '1B', 'Im', 'At', '4h', '6t']

    for sub1 in substrings:
        for sub2 in substrings:
            for sub3 in substrings:

                passwd = sub1 + sub2 + sub3
                c_pwd = crypt.crypt(passwd, salt)

                if cryptPasswd == c_pwd:
                    return passwd

    print "Could not decrypt", cryptPasswd

def crackMultiple(cryptPasswds):
    """Returns list of corresponding string cracked passwords"""
    passwords = []

    for cPass in cryptPasswds:
        p = crack(cPass)
        passwords.append(p)

    return passwords

def main():

    #Start timer
    start = time.time()
    print("Starting timer")

    #sortPasswds('../passOnly0')
    #getAllSubstrs('../passOnly0')
    cryptPasswd = 'tooyyY4AWoRMw'
    crack(cryptPasswd)

    #Stop and print timer
    end = time.time()
    print(end - start, "seconds")

if __name__ == '__main__':
    main()