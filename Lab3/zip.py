#!/usr/bin/env python3

import time
import zipfile

PASSWORD = 'fluffy'
ZIP_NAME = 'key.zip'
FILE_NAME = 'key'

OUT_FILE = 'obfuscated.txt'

#https://docs.python.org/3/library/zipfile.html

def main():

    #https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    PWD = str.encode(PASSWORD)

    start = time.time()
    print("Starting timer")

    with zipfile.ZipFile(ZIP_NAME) as myzip:
        myzip.setpassword(PWD)
        with myzip.open(FILE_NAME, 'r') as myfile:
            reading = myfile.read()

            #Open output files
            file = open(OUT_FILE, "wb")
            file.write(reading)
            file.close()

    end = time.time()
    print(end - start, "seconds")               


if __name__ == '__main__':
    main()

    