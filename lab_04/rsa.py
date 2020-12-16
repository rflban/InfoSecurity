import math
import random

from random import randrange


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def egcd(a, b):
    x0, y0 = 0, 1
    x1, y1 = 1, 0
    a0, b0 = a, b

    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x0, x1) = ((x1 - (q * x0)), x0)
        (y0, y1) = ((y1 - (q * y0)), y0)

    if x1 < 0:
        x1 += b0
    if y1 < 0:
        y1 += a0

    return x1, y1


def isPrime(n):
    lowPrimes = [
          2,   3,   5,   7,  11,  13,  17,  19,  23,  29,  31,  37,  41,  43,
         47,  53,  59,  61,  67,  71,  73,  79,  83,  89,  97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
        191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
        269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
        353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,
        439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521,
        523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
        617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
        709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
        811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
        907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
    ]

    if n == 2:
        return True

    if n >= 3:
        if n & 1: # если нечетное
            for p in lowPrimes:
                if (n == p):
                    return True
                if (n % p == 0):
                    return False

            for num in range(2, int(math.sqrt(n))):
                if n % num == 0:
                    return False

            return True

    return False


class RSA:
    def __init__(self, keySize=10, random_seed=None):
        if random_seed is not None:
            random.seed(random_seed)

        self._pub, self._pri = RSA.genKeypair(keySize)

    def genPrime(k):
         while True:
             n = random.randrange(2**(k-1), 2**(k))
             if isPrime(n) == True:
                 return n

    def genKeypair(keySize=10):
        p = q = RSA.genPrime(keySize)

        while p == q:
            q = RSA.genPrime(keySize)

        n = p*q # длина алфавита
        phi = (p - 1)*(q - 1)

        # выбираем е взаимно простое с phi
        e = random.randrange(1, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(1, phi)

        # поиск закрытого ключа как решения уравнения (E*D) % phi = 1
        # E*D + phi*k = 1
        d = egcd(e, phi)[0]
        if d < 0:
            d += e

        #открытый ключ (e, n) и закрытый ключ (d, n)
        return ((e, n), (d, n))

    def encrypt(self, plainbytes):
        key, n = self._pub
        cipher = [pow(byte, key, n) for byte in plainbytes]

        cipherbytes = b''
        for num in cipher:
            cipherbytes += num.to_bytes(4, 'little')

        return cipherbytes

    def decrypt(self, cipherbytes):
        cipher = []
        for i in range(0, len(cipherbytes), 4):
            cipher.append(int.from_bytes(cipherbytes[i:i+4], 'little'))

        key, n = self._pri
        plain = [pow(byte, key, n) for byte in cipher]

        return bytearray(plain)
