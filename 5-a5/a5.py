from collections.abc import Generator, Iterator
from functools import reduce
from typing import List, Tuple


# https://en.wikipedia.org/wiki/A5/1
class A5:
    R_BITS = [19, 22, 23]
    _FEEDBACK_BIT_INDEXES_LISTS = [[13, 16, 17, 18], [20, 21], [7, 20, 21, 22]]
    _SYNC_BIT_INDEXES = [8, 10, 10]

    RegisterGenerator = Generator[Tuple[bool, bool], bool, None]

    @staticmethod
    def register_generator(register: List[bool], feedback_bit_indexes: List[int], sync_bit_index: int) -> \
            RegisterGenerator:
        prev_output = False
        prev_sync_bit = False
        common_sync_bit = False
        while True:
            if prev_sync_bit == common_sync_bit:
                register.append(prev_output)
                register.pop(0)

            feedback_bits = [bit for index, bit in enumerate(register)
                             if index in feedback_bit_indexes]
            prev_output = reduce(bool.__xor__, feedback_bits)
            prev_sync_bit = register[sync_bit_index]
            yield prev_output, prev_sync_bit
            common_sync_bit = yield

    @staticmethod
    def multiregister(r1: RegisterGenerator, r2: RegisterGenerator, r3: RegisterGenerator) -> \
            Iterator[bool]:
        def sync_function(b1: bool, b2: bool, b3: bool):
            return b1 & b2 | b1 & b3 | b2 & b3

        for (o1, s1), (o2, s2), (o3, s3) in zip(r1, r2, r3):
            output = o1 ^ o2 ^ o3
            sync_bit = sync_function(s1, s2, s3)
            r1.send(sync_bit)
            r2.send(sync_bit)
            r3.send(sync_bit)
            yield output

    def __init__(self, r1_seed: List[bool], r2_seed: List[bool], r3_seed: List[bool]):
        self._seeds = [r1_seed, r2_seed, r3_seed]

    def create_generator(self) -> Iterator[bool]:
        gens = [A5.register_generator(list(seed), lst, sync_bit_index) for seed, lst, sync_bit_index in
                zip(self._seeds, A5._FEEDBACK_BIT_INDEXES_LISTS, A5._SYNC_BIT_INDEXES)]
        return A5.multiregister(*gens)


class XorEncoder:
    @staticmethod
    def encrypt(text: List[bool], key_iterator: Iterator[bool]) -> List[bool]:
        return [text_bit ^ key_bit for text_bit, key_bit in zip(text, key_iterator)]

    @staticmethod
    def decrypt(text: List[bool], key_iterator: Iterator[bool]) -> List[bool]:
        return XorEncoder.encrypt(text, key_iterator)


def main():
    from random import randint
    text = [bool(randint(0, 1)) for _ in range(50)]
    r1 = [bool(randint(0, 1)) for _ in range(A5.R_BITS[0])]
    r2 = [bool(randint(0, 1)) for _ in range(A5.R_BITS[1])]
    r3 = [bool(randint(0, 1)) for _ in range(A5.R_BITS[2])]
    a5 = A5(r1, r2, r3)
    encrypted = XorEncoder.encrypt(text, a5.create_generator())
    # print(text)
    # print(encrypted)
    decrypted = XorEncoder.decrypt(encrypted, a5.create_generator())
    assert decrypted == text


if __name__ == '__main__':
    main()
