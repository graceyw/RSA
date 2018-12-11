#!/usr/bin/env python
""" attempts a partial key attack on an RSA key -- only works on single example because of difficulty with LSBs """

import math
import datetime

class PartialKeyExposureAttack:

	def __init__(self, N, e):
		""" initializes partial key exposure algorithm """

		# when we create the attack object, we initialize it with the public RSA information we already know
		self.N = N # the product of p and q
		self.n = len(format(N, 'b')) # the length of N in bits
		self.e = e # the public key

		# we carry out a fake timing attack to obtain at least a quarter of the least significant bits (LSBSs) of d, the private key;
		# it doesn't matter how we get the LSBs (ex. if they're hard-coded), but the algorithm requires them.
		self.exposed_lsbs = self.fake_timing_attack()

		# once we solve for the rest of the private key, we will populate this value.
		self.d = None # the private key


	def fake_timing_attack(self):
		""" simulates timing attack or other method of partially exposing a key """

		# these three LSBs were provided as part of the example we followed while implementing this algorithm;
		# the code below finds the lowest-order-bits of whatever N was given, but the implementation failed
		# when the lowest-order-bits were used. Either the numerical example we followed misinformed our
		# implementation, or the lowest-order-bits are not actually the LSBs.
		return '011'

		### largest_possible_binary_string = format(self.N, 'b')
		### required_number_of_lsb = int(math.ceil(len(largest_possible_binary_string)/ 4.0))
		### lsbs = largest_possible_binary_string[len(largest_possible_binary_string) - required_number_of_lsb:]
		### return lsbs


	def find_private_key(self):
		""" calculates the private key """
		
		# to solve for the private key using the partial private key, we're using the equation e*d_0 = 1 + k*(N - s + 1) mod(2^(n/4)). 
		# This equation is an adaptation of the Euler-inspired e*d = 1 mod(phi N) used to calculate the private key in RSA. 
		# 1 mod(phi N) equates to 1 + k*(phi N) when e*d = 1 mod(phi N) is written as a linear combination of e*d and phi N, and
		# 1 + k*(phi N) is equivalent to 1 + k*(N - s + 1). That means that e*d = 1 mod(phi N) = 1 + k*(N - s + 1).
		# to account for the use of a partial private key, d_0, instead of the full private key, d, we substitute d = d_0 mod(2^(n/4)).
		# if we move mod(2^(n/4)) to the other side of the equation, we end up with e*d_0 = 1 + k*(N - s + 1) mod(2^(n/4)).

		# now, that we understand where the equation came from, let's solve for the key

		# we'll start by simplifying some of the components to make the code more readable
		d_0 = int(self.exposed_lsbs, 2) # we convert the exposed bits of the private key into an integer
		modulus = 2 ** len(self.exposed_lsbs) # the modulus represents 2 ^ (n/4); we solve that here to make the code more readable later

		# in the line of code below, we solve and simplify the LHS of the partial key attack equation.
		# we "wrap" the value of e * d_0 by finding the remainder of e * d_0 mod 2 ^ (n/4) and move the 1 from the RHS to the LHS
		# to further simplify the equation components as much as possible before diving into the algorithm.
		lhs = self.e * d_0 % modulus - 1 

		# there are two variables in the RHS [k*(N - s + 1) mod(2^(n/4))] that we don't know -- k and s (assume that s = p + q).
		# so, we begin the attack by running through values of k until we get to the correct value of s.
		# we'll know we're at the right value of s when we can solve for a valid p such that p^2 - s*p + N = 0 mod(2^(n/4)).
		# since phi(N) > d, we know that k < e from the linear combination e*d = k*(phi N), 
		# so at most we need to run through e values to find the right k, s, and p.
		for k in range(self.e):
			
			# given a certain value of k, we solve for s in e*d_0 = 1 + k*(N - s + 1) mod(2^(n/4))
			s = ((k * (self.N + 1) - lhs) % modulus)
			
			# now, we need to figure out if this is the right s value by solving for p. To solve for p, we'll run through every
			# number up to the value of the modulus, 2^(n/4), - 1 until a number satisfies the equation.
			p_rhs = -self.N % modulus # to improve readability, we solve a simplified version of the RHS now
			
			for p in range(modulus):

				# for each value of p, we check to see if the LHS of the equation matches the pre-calculated RHS
				if p * (p - s) == p_rhs:
					p_0 = p # if the two sides match, then we know we have the correct p value, so we set p_0 = p for the next equation (confusing syntax)

					# to get the factors of N, we need to solve f(x, y) = (2^(n/4)*x + p_0)(2^(n/4)*y + q_0) - N.
					# before we can do that, we need to find q_0 such that p_0*q_0 = N mod(2^(n/4)).
					# we'll do this the same way we solved for p_0 -- by running through every value of q_0 up to 2^(n/4) - 1 until we get the right q_0
					for q in range(modulus):
						if p_0 * q % modulus == self.N % modulus:
							q_0 = q # if the two sides match, then we know we have the correct q value
							break

					# now we have the information we need to solve f(x, y) = (2^(n/4)*x + p_0)(2^(n/4)*y + q_0) - N.
					# again, we'll run through every value of x and see if the resulting value of y is an integer (which means x and y are factors)
					# until we get a match. Then we can solve for the factors of N, p and q.
					for x in range(modulus):
						y = (self.N - modulus * x * p_0 - p_0 * q_0) / ((modulus ** 2.0) * x + modulus * q_0) # the 2.0 is necessary bc it needs to be a float for is_integer()
						if y.is_integer():
							p = modulus * x + p_0
							q = modulus * y + q_0
							phi_n = (p - 1) * (q - 1) # now that we have the factors of N, we can calculate phi N
							self.d = int((1 + k * phi_n) / self.e) # we solve for the full private key, d, with k and phi N
							return		


	# the encryption and decryption functions below were used for testing;
	# an extended explanation of how they work is included in Appendix E.
	def encrypt_message(self, message):
		""" uses the public information to encrypt a message """
		cipher = message ** self.e % self.N
		return cipher

	def decrypt_message(self, cipher):
		""" uses the already-found private key to decipher ciphers """
		message = cipher ** self.d % self.N
		return message


# the following commands are carried out when the script is run
if __name__ == "__main__":

	# initialize partial key exposure attack with public information
	partial_key_exposure_attack = PartialKeyExposureAttack(N = 1633, e = 23) # 80-120 microseconds

	# benchmark how long it takes to break the key in microseconds
	benchmark_start = datetime.datetime.now()
	partial_key_exposure_attack.find_private_key()
	benchmark_time = datetime.datetime.now() - benchmark_start
	print ("benchmark timed:", benchmark_time.microseconds)

	# check to make sure the private key is correct by decrypting a cipher
	cipher = partial_key_exposure_attack.encrypt_message(message = 1234) # the value of the message M must be <N
	message = partial_key_exposure_attack.decrypt_message(cipher = cipher)
	print ("private key:", partial_key_exposure_attack.d, "decrypted message:", int(message))