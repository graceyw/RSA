""" attempts a brute force attack on an RSA key -- uses a victim's public key and n to find their private key and decrypt their messages"""

import datetime

class BruteForceAttack:

	def __init__(self, n, e):
		""" initializes brute force algorithm with the victim's public information """
		self.known_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,
			103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,
			199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,
			313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,
			433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,
			563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,
			673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,
			811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,
			941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,
			1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,
			1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,
			1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,
			1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471,1481,1483,1487,
			1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583,1597,
			1601,1607,1609,1613,1619,1621,1627,1637,1657,1663,1667,1669,1693,1697,1699,
			1709,1721,1723,1733,1741,1747,1753,1759,1777,1783,1787,1789,1801,1811,1823,
			1831,1847,1861,1867,1871,1873,1877,1879,1889,1901,1907,1913,1931,1933,1949,
			1951,1973,1979,1987,1993,1997,1999,2003,2011,2017,2027,2029,2039,2053,2063]
		self.hidden_primes_product = n
		self.public_key = e
		self.private_key = None


	def find_private_key(self):
		""" calls helper functions to find the hidden primes and private key via brute force"""
		p, q = self.find_hidden_primes()
		self.private_key = self.calculate_private_key(p, q)
		return self.private_key


	def calculate_private_key(self, p, q):
		""" uses the half-extended Euclidean algorithm to solve for the private key """
		m = (p - 1) * (q - 1)

		a = self.public_key
		b = m
		x = 0
		y = 1

		while True:
			if a == 1:
				return y
			elif a == 0:
				return None

			q = b / a
			b = b - a * q
			x = x + q * y

			if b == 1:
				return m - x
			elif b == 0:
				return NoneW\

			q = a / b
			a = a - b * q
			y = y + q * x


	def find_hidden_primes(self):
		""" goes through all of the known primes to see if any of them evenly divides the product """
		for prime in self.known_primes:
			if self.hidden_primes_product % prime == 0:
				other_factor = self.hidden_primes_product / prime
				if other_factor in self.known_primes:
					return (prime, other_factor)

		print ("p and q exceed the known primes")


	def decrypt_message(self, cipher):
		""" uses the already-found private key to decipher ciphers """
		message = cipher ** self.private_key % self.hidden_primes_product
		return message

	
	def encrypt_message(self, message):
		""" just for testing """
		cipher = message ** self.public_key % self.hidden_primes_product
		return cipher


if __name__ == "__main__":
	# initialize brute force attack with public information
	brute_force_algorithm = BruteForceAttack(n = 226679, e = 2737) # p = 419, q = 541 -- 35-70 microseconds

	# benchmark how long it takes to break the key
	benchmark_start = datetime.datetime.now()
	brute_force_algorithm.find_private_key()
	benchmark_time = datetime.datetime.now() - benchmark_start
	print (benchmark_time.microseconds)

	# ensure it can correctly decipher messages
	cipher = brute_force_algorithm.encrypt_message(message = 123456) # m < n
	message = brute_force_algorithm.decrypt_message(cipher = cipher)
	print ("private key:", brute_force_algorithm.private_key, "decrypted message:", int(message))
