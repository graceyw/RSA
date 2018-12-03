""" attempts a brute force attack on an RSA key -- uses a victim's public key and n to find their private key and decrypt their messages"""

class BruteForceAttack:

	def __init__(self, n, e):
		""" initializes brute force algorithm with the victim's public information """
		self.known_primes = [2, 3, 5, 7, 11, 13, 17, 19]
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
				return None

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


if __name__ == "__main__":
	brute_force_algorithm = BruteForceAttack(n = 33, e = 7)
	brute_force_algorithm.find_private_key()
	message = brute_force_algorithm.decrypt_message(cipher = 4)
	print ("private key:", brute_force_algorithm.private_key, "decrypted message:", message)
