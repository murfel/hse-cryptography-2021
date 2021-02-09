from typing import List


def bool_to_binstring(text: List[bool]) -> str:
    return ''.join(list(map(lambda x: str(int(x)), text)))


class AESEncryption:
    BLOCK_SIZE_BITS = 128
    KEY_SIZES_BITS = [128, 192, 256]

    @staticmethod
    def encrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == AESEncryption.BLOCK_SIZE_BITS
        assert len(key) in AESEncryption.KEY_SIZES_BITS
        return []

    @staticmethod
    def decrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == AESEncryption.BLOCK_SIZE_BITS
        assert len(key) in AESEncryption.KEY_SIZES_BITS
        return []


def main():
    from random import randint
    text = [bool(randint(0, 1)) for _ in range(AESEncryption.BLOCK_SIZE_BITS)]
    key = [bool(randint(0, 1)) for _ in range(AESEncryption.KEY_SIZES_BITS[0])]
    key_copy = list(key)
    encrypted = AESEncryption.encrypt(text, key)
    decrypted = AESEncryption.decrypt(encrypted, key_copy)
    assert decrypted == text


if __name__ == '__main__':
    main()
