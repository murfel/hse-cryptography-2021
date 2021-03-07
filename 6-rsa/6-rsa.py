import random
from typing import Tuple


def gcd(a: int, b: int) -> int:
    r0, r1 = a, b
    while r1 != 0:
        q = r0 // r1
        r2 = r0 - q * r1
        r0, r1 = r1, r2
    return r0


def ext_gcd(a: int, b: int) -> Tuple[int, int, int]:
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r2 = r0 - q * r1
        s2 = s0 - q * s1
        t2 = t0 - q * t1
        r0, r1 = r1, r2
        s0, s1 = s1, s2
        t0, t1 = t1, t2
    return r0, s0, t0


def bin_pow_modulo(base, power, modulo):
    if power == 0:
        return 1
    if power == 1:
        return base
    square = bin_pow_modulo(base, power // 2, modulo) ** 2 % modulo
    if power % 2 == 1:
        square = square * base % modulo
    return square


def generate_random_coprime(number: int, iterations: int = 10 ** 6) -> int:
    for _ in range(iterations):
        possible_coprime = random.randrange(1, number)
        if gcd(number, possible_coprime) == 1:
            return possible_coprime
    return -1


class PrimeNumberGenerator:
    @staticmethod
    def _check_witness_confirms_primeness(witness: int, number: int) -> bool:
        return bin_pow_modulo(witness, number - 1, number) == 1

    @staticmethod
    def _is_possibly_prime_fermat(number: int) -> bool:
        for _ in range(100):
            possible_witness = generate_random_coprime(number, 100)
            if possible_witness == -1:
                return False
            elif PrimeNumberGenerator._check_witness_confirms_primeness(possible_witness, number):
                continue
            else:
                return False
        return True

    @staticmethod
    def gen_prime_number():
        while True:
            number = random.randrange(10 ** 5, 10 ** 7)
            if PrimeNumberGenerator._is_possibly_prime_fermat(number):
                return number


class RSAEncrypter:
    def __init__(self, modulo, exponent):
        self._modulo = modulo
        self._exponent = exponent

    def encrypt(self, message: int) -> int:
        return bin_pow_modulo(message, self._exponent, self._modulo)


class RSADecrypter:
    def __init__(self):
        prime1 = PrimeNumberGenerator.gen_prime_number()
        prime2 = PrimeNumberGenerator.gen_prime_number()
        self._modulo = prime1 * prime2
        self._euler_phi_function = (prime1 - 1) * (prime2 - 1)
        self._public_exponent = generate_random_coprime(self._euler_phi_function)
        self._private_exponent = ext_gcd(self._public_exponent, self._euler_phi_function)[1]

    def get_public_key(self) -> Tuple[int, int]:
        return self._modulo, self._public_exponent

    def decrypt(self, encrypted_message: int) -> int:
        return bin_pow_modulo(encrypted_message, self._private_exponent, self._modulo)


def main():
    decrypter = RSADecrypter()
    public_key_modulo, public_key_exponent = decrypter.get_public_key()
    message = random.randrange(public_key_modulo)
    encrypted = RSAEncrypter(public_key_modulo, public_key_exponent).encrypt(message)
    decrypted = decrypter.decrypt(encrypted)
    assert message == decrypted


if __name__ == '__main__':
    main()
