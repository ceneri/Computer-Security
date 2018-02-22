
import time
import crypt
from threading import Thread 
import multiprocessing as mp


CRYPT = 'nuCaRpTeLXVOg'

def get_salt(password):
    return password[0:2]

def get_alphabet():

    numbers = list(range(48,58))
    uppercase = list(range(65,91))
    lowercase = list(range(97,123))

    alphabet = numbers + uppercase + lowercase

    #Turn list of numbers, into list of chars
    for i in range( len(alphabet) ):
        alphabet[i] = chr(alphabet[i])

    return alphabet


def crack_single(password, indexStart, indexEnd, queue):

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
                            
                            #print (pwd)



#https://pymotw.com/3/threading/
#https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing
#https://docs.python.org/3.5/library/multiprocessing.html


def main():

    start = time.time()
    print("Starting timer")

    queue = mp.Queue()

    indexes = [ (CRYPT, 0, 8, queue), (CRYPT,8, 16, queue),  (CRYPT, 16, 24, queue), (CRYPT, 24, 32, queue),
                (CRYPT, 32, 40, queue), (CRYPT,40, 48, queue),  (CRYPT, 48, 55, queue), (CRYPT, 55, 62, queue)
                ]

    no_thread = len(indexes)

    threads = []
    for i in range(no_thread):
        t = mp.Process(target=crack_single, args=(indexes[i]) )
        threads.append(t)
        t.start()

    while True:
        time.sleep(10)
        if queue.get() == "Done":
            for i in range(no_thread):
                threads[i].terminate() 
            break

    for i in range(no_thread):
        threads[i].join()


    end = time.time()
    print(end - start, "seconds")				


if __name__ == '__main__':
	main()