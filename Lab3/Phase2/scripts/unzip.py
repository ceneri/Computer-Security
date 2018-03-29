#!/usr/bin/env python3

import zipfile


KEY_FILE = 'key'

#https://docs.python.org/3/library/zipfile.html

def unzipFile(zipFilename, outputFileName, password):

    #https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    PWD = str.encode(password)

    with zipfile.ZipFile(zipFilename) as myzip:
        myzip.setpassword(PWD)
        with myzip.open(KEY_FILE, 'r') as myfile:
            reading = myfile.read()

            #Open output files
            file = open(outputFileName, "wb")
            file.write(reading)
            file.close()



if __name__ == '__main__':
    main()

    