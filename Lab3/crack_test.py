
import time
import crypt 


numbers = list(range(48,58))
uppercase = list(range(65,91))
lowercase = list(range(97,123))

alphabet = numbers + uppercase + lowercase


def main():

	start = time.time()
	print("Starting timer")

	#Turn list of numbers, into list of chars
	for i in range( len(alphabet) ):
		alphabet[i] = chr(alphabet[i])

	
	a = '0'
	b = '0'
	for c in alphabet:
		for d in alphabet:
			for e in alphabet:
				for f in alphabet:

					pwd = a+b+c+d+e+f
					crypt.crypt(pwd, 'lol')
					#print (pwd)


	end = time.time()
	print(end - start, "seconds")					


if __name__ == '__main__':
	main()