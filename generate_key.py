import math
import random

'''Pick 2 random primes (have size as a changeable input?)'''


def prime_generator(upper_bound):
    # create a prime generator
    return [1, 2, 3, 5]


def prime_picker(upper_bound):
    # use prime generator
    prime_list = prime_generator(upper_bound)
    # pick 2 random numbers before upper bound and return the values @ the index
    return (5, 7)


def generate_public_key(p, q):
    # ask Sara about how to do/explain why it works



'''Find least common multiple'''

'''Generate public key e: Choose a positive integer e that’s < LCM and coprime with LCM'''

'''Generate private key d: Find the modular multiplicative inverse d of (e mod LCM) s.t. the remainder after dividing d * e by LCM is 1'''


def generate_private_keys():
    p, q = prime_picker()
    n = p*q


def encrypt():



def decrypt():
