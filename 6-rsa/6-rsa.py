from typing import Tuple


class RSAEncrypter:
    @staticmethod
    def encrypt(plain_message: int, n: int, exp: int) -> int:
        pass


class RSADecrypter:
    def __init__(self):
        self._prime1 = 0
        self._prime2 = 0
        self._modulo = self._prime1 * self._prime2
        self._public_exponent = 0
        self._private_exponent = 0

    def get_public_key(self) -> Tuple[int, int]:
        return self._modulo, self._public_exponent

    def decrypt(self, encrypted_message: int) -> int:
        pass


def main():
    import random
    decrypter = RSADecrypter()
    public_key_modulo, public_key_exponent = decrypter.get_public_key()
    message = random.randrange(public_key_modulo)
    encrypted = RSAEncrypter.encrypt(message, public_key_modulo, public_key_exponent)
    decrypted = decrypter.decrypt(encrypted)
    assert message == decrypted


if __name__ == '__main__':
    main()
