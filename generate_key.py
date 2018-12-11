import math
import random


'''Pick 2 random primes (have size as a changeable input?)'''

def prime_generator(upperBound = math.inf):
    '''
    INPUT: upperBound (the largest acceptable prime) is infinity by default.
    We'll use a specific value if we want there to be an upper limit, specifically
    when generating the public key.
    OUTPUT: A list of primes that are all <= upperBound.
    '''
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,
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

    '''This loop iterates through the above list, locating the index of the
    upperBound prime and returning the list of primes up to that index.
    Certainly not the most efficient way to do this, but because we're not
    working with very many primes right now, it gets the job done. We'd want
    to change this to perhaps start at primes[primes.length()/2] and then continue
    cutting into the appropriate half until the prime is found.'''

    if upperBound != math.inf:
        index = 0
        for i in primes:
            if i <= upperBound:
                index += 1
        return primes[0:index+1]
    else:
        return primes


def prime_picker(upperBound = math.inf):
    '''INPUT: Large prime number which is > both the chosen primes.
    OUTPUT: 2 random primes < upperBound, chosen from the list generated in prime_generator.'''
    options = prime_generator(upperBound)    # use list generated in prime_generator
    chosen1 = random.choice(options)
    chosen2 = random.choice(options)   # TODO: Does it matter if chosen primes are the same?
    return chosen1,chosen2


def generate_public_key(p,q):
    '''INPUT: 2 primes p and q.
    OUTPUT: A public key.'''
    n = p*q
    phi = (p-1)*(q-1)  # This relationship is why we need to use prime numbers...ensure we know how to explain this.
    keyOptions = prime_generator(phi)
    publicKey = random.choice(keyOptions)
    while math.gcd(phi,publicKey) != 1:
        publicKey = random.choice(keyOptions)   # If the GCD isn't 1, choose a different key
    return publicKey


def generate_private_key(publicKey,p,q):
    '''
    INPUT: A publicKey (generated in generate_public_key(p,q)) and the primes chosen p and q.
    To generate the private key, this function finds the modular multiplicative inverse d of
    (e mod LCM) s.t. the remainder after dividing d * e by LCM is 1. Uses the half-extended
    Euclidean algorithm to solve for the private key.
    OUTPUT: A private key.'''
    m = (p - 1) * (q - 1)

    a = generate_public_key(p,q)
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


def encrypt(upperBound = math.inf):
    '''
    This is the only function we need to call in order to produce the public and private keys.
    INPUT: An upperBound, which is infinity by default unless replaced in the function call.
    OUTPUT: A public key and a private key.'''
    p,q = prime_picker(upperBound)
    publicKey = generate_public_key(p,q)
    return ("Public key: " + str(publicKey),
            "Private key: " + str(generate_private_key(publicKey,p,q)))


if __name__ == '__main__':
    print(encrypt(2011))
