#!/usr/bin/env python3

"""Sources Used:
    #https://pymotw.com/3/threading/
    #https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing
    #https://docs.python.org/3.5/library/multiprocessing.html
"""

import sys
import time
import crypt
from threading import Thread 
import multiprocessing as mp

DICTIONARY_FILE = "words.txt"

def get_salt(password):
    return password[0:2]

def get_dictionary():
    dictionary = []

    file = open(DICTIONARY_FILE, "r")

    for line in file:
        dictionary.append(line[:-1])

    file.close()
    return dictionary


def dictionary_attack(password):

    print ("Encrypted:", password)

    salt = get_salt(password)

    print ("Salt:", salt)

    dictionary = get_dictionary()

    #Search for password
    for line in dictionary:
        if crypt.crypt(line, salt) == password:
            return line
        elif crypt.crypt(line.lower(), salt) == password:
            return line.lower()
        elif crypt.crypt(line.upper(), salt) == password:
            return line.upper()
        elif crypt.crypt(line.title(), salt) == password:
            return line.title()

    #Password not found
    return None   

def get_alphabet():

    numbers = list(range(48,58))
    uppercase = list(range(65,91))
    lowercase = list(range(97,123))

    alphabet = numbers + uppercase + lowercase

    #Turn list of numbers, into list of chars
    for i in range( len(alphabet) ):
        alphabet[i] = chr(alphabet[i])

    return alphabet


def brute_force(password, indexStart, indexEnd, queue):

    salt = get_salt(password)

    alphabet = get_alphabet()

    for i in range(indexStart, indexEnd):
        a = alphabet[i]
        for b in alphabet:
            for c in alphabet:
                for d in alphabet:
                    for e in alphabet:
                        for f in alphabet:

                            pwd = a+b+c+d+e+f
                            c_pwd = crypt.crypt(pwd, salt)

                            if password == c_pwd:
                                print ("Password:", pwd)

                                queue.put("Done")


def main():

    #Start timer
    start = time.time()
    print("Starting timer")

    #Get encrypted password parameter
    CRYPT = sys.argv[1]

    #Attempt to find by dictionary attack
    password = dictionary_attack(CRYPT)

    #If dictionary is unsuccesful, then do brute force
    if password == None:

        #Queue used to pass information from child process to parent
        queue = mp.Queue()

        #Range/Indexes to be assigned to each thread, for now they are hard coded (8 processes)
        indexes = [ (CRYPT, 0, 8, queue), (CRYPT,8, 16, queue),  (CRYPT, 16, 24, queue), (CRYPT, 24, 32, queue),
                    (CRYPT, 32, 40, queue), (CRYPT,40, 48, queue),  (CRYPT, 48, 55, queue), (CRYPT, 55, 62, queue)
                    ]

        num_processes = len(indexes)

        #Create child processes with brute_force function and specified range
        processes = []
        for i in range(num_processes):
            p = mp.Process(target=brute_force, args=(indexes[i]) )
            processes.append(p)
            p.start()

        #Every minute check if a process succesfully found password, if so kill every child process (DONE)
        while True:
            time.sleep(60)
            if queue.get() == "Done":
                for i in range(num_processes):
                    processes[i].terminate() 
                break

        #Necessary Join
        for i in range(num_processes):
            processes[i].join()

    else:
        print("Password:", password)

    #Stop and print timer
    end = time.time()
    print(end - start, "seconds")				


if __name__ == '__main__':
	main()