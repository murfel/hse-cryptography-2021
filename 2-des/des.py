from typing import List

def bool_to_binstring(text: List[bool]) -> str:
    return ''.join(list(map(lambda x: str(int(x)), text)))


class DESEnctyption:
    # https://en.wikipedia.org/wiki/Data_Encryption_Standard#Description
    # https://ru.wikipedia.org/wiki/DES#Схема_шифрования_алгоритма_DES
    BLOCK_SIZE = 64
    KEY_LEN = 56
    NUM_STEPS = 16
    INITIAL_PERMUTATION = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    REVERSE_PERMUTATION = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
    EXTENSION_PERMUTATION = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    FEISTEL_PERMUTATION = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    S_PERMUTATIONS = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
                      [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
                      [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
                      [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
                      [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
                      [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
                      [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
                      [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    KEY_PERMUTATION = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    KEY_SHIFT_VALUE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    CHOOSE_KEY_BITS_PERMUTATION = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    PERMS = [INITIAL_PERMUTATION, REVERSE_PERMUTATION, EXTENSION_PERMUTATION, FEISTEL_PERMUTATION, KEY_PERMUTATION, CHOOSE_KEY_BITS_PERMUTATION]

    for perm in PERMS:
        for i in range(len(perm)):
            perm[i] -= 1

    for i, row in enumerate(S_PERMUTATIONS):
        for perm in row:
            assert len(perm) == 16

    @staticmethod
    def _apply_perm(text: List[bool], permutation: List[int]) -> List[bool]:
        return [text[index] for index in permutation]

    @staticmethod
    def _apply_perm_rev(text: List[bool], permutation: List[int]) -> List[bool]:
        new_text = [False for _ in range(max(permutation))]
        for i, p in enumerate(permutation):
            new_text[p] = text[i]
        return new_text

    @staticmethod
    def _preprosess_key(key: List[bool]) -> List[bool]:
        assert len(key) == 56
        for i in range(1, 9):
            key.insert(i * 8 - 1, False)
        return DESEnctyption._apply_perm(key, DESEnctyption.KEY_PERMUTATION)

    @staticmethod
    def _left_shift(arr: List[bool], num: int) -> List[bool]:
        shifted_arr = list(arr)
        for _ in range(num):
            shifted_arr.append(shifted_arr[0])
            shifted_arr.pop(0)
        return shifted_arr

    @staticmethod
    def _calc_next_key_seed(key_seed: List[bool], step: int) -> List[bool]:
        assert len(key_seed) == 56
        assert 0 <= step <= 15
        left_key, right_key = key_seed[:28], key_seed[28:]
        shift_value = DESEnctyption.KEY_SHIFT_VALUE[step]
        left_key = DESEnctyption._left_shift(left_key, shift_value)
        right_key = DESEnctyption._left_shift(right_key, shift_value)
        return left_key + right_key

    @staticmethod
    def _calc_next_key(key_seed: List[bool]) -> List[bool]:
        return DESEnctyption._apply_perm(key_seed, DESEnctyption.CHOOSE_KEY_BITS_PERMUTATION)

    @staticmethod
    def _calc_all_keys(key: List[bool]) -> List[List[bool]]:
        assert len(key) == 56
        key_seed = DESEnctyption._preprosess_key(key)
        assert len(key_seed) == 56
        keys = []
        for step in range(DESEnctyption.NUM_STEPS):
            key_seed = DESEnctyption._calc_next_key_seed(key_seed, step)
            assert len(key_seed) == 56
            keys.append(DESEnctyption._apply_perm(key_seed, DESEnctyption.CHOOSE_KEY_BITS_PERMUTATION))
        return keys

    @staticmethod
    def _xor(op1: List[bool], op2: List[bool]) -> List[bool]:
        assert len(op1) == len(op2)
        ans = [b1 ^ b2 for b1, b2 in zip(op1, op2)]
        assert len(ans) == len(op1)
        return ans

    @staticmethod
    def _choose_s_permutation(text: List[bool], round_index: int) -> List[bool]:
        assert len(text) == 6
        assert 0 <= round_index <= 15
        s_perm = DESEnctyption.S_PERMUTATIONS[round_index]
        row = int(str(int(text[0])) + str(int(text[-1])), 2)
        col = int(''.join(map(lambda x: str(int(x)), text[1:-1])), 2)
        number = s_perm[row][col]
        ans = list(map(lambda x: bool(int(x)), list(format(number, '04b'))))
        assert len(ans) == 4
        return ans

    @staticmethod
    def _flatten(arr: List[List[bool]]) -> List[bool]:
        return [item for sublist in arr for item in sublist]

    @staticmethod
    def _break_into_blocks(arr: List[bool]) -> List[List[bool]]:
        pass

    @staticmethod
    def _feistel_function(half_text: List[bool], key: List[bool]) -> List[bool]:
        assert len(half_text) == 32
        assert len(key) == 48
        half_text = DESEnctyption._apply_perm(half_text, DESEnctyption.EXTENSION_PERMUTATION)
        assert len(half_text) == 48
        half_text = DESEnctyption._xor(half_text, key)
        blocks = []
        S_BLOCK_LEN = 6
        NUM_S_BLOCKS = 8
        for i in range(NUM_S_BLOCKS):
            block = half_text[i * S_BLOCK_LEN: (i+1) * S_BLOCK_LEN]
            assert len(block) == S_BLOCK_LEN
            blocks.append(DESEnctyption._choose_s_permutation(block, i))
        assert len(blocks) == NUM_S_BLOCKS
        half_text = DESEnctyption._flatten(blocks)
        assert len(half_text) == 32
        half_text = DESEnctyption._apply_perm(half_text, DESEnctyption.FEISTEL_PERMUTATION)
        return half_text

    @staticmethod
    def des_encrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == 64
        assert len(key) == 56
        keys = DESEnctyption._calc_all_keys(key)
        text = DESEnctyption._apply_perm(text, DESEnctyption.INITIAL_PERMUTATION)
        l_prev, r_prev = text[:32], text[32:]
        for step in range(DESEnctyption.NUM_STEPS):
            key = keys[step]
            l = r_prev
            r = DESEnctyption._xor(l_prev, DESEnctyption._feistel_function(r_prev, key))
            l_prev, r_prev = l, r
        text = l_prev + r_prev
        text = DESEnctyption._apply_perm(text, DESEnctyption.REVERSE_PERMUTATION)
        return text

    @staticmethod
    def des_decrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == 64
        assert len(key) == 56
        keys = DESEnctyption._calc_all_keys(key)
        text = DESEnctyption._apply_perm(text, DESEnctyption.INITIAL_PERMUTATION)
        l, r = text[:32], text[32:]
        for step in reversed(range(DESEnctyption.NUM_STEPS)):
            r_prev = l
            l_prev = DESEnctyption._xor(r, DESEnctyption._feistel_function(l, keys[step]))
            l = l_prev
            r = r_prev
        text = l + r
        text = DESEnctyption._apply_perm(text, DESEnctyption.REVERSE_PERMUTATION)
        return text


def main():
    from random import randint
    text = [bool(randint(0, 1)) for _ in range(64)]
    key = [bool(randint(0, 1)) for _ in range(56)]
    key_copy = list(key)
    encrypted = DESEnctyption.des_encrypt(text, key)
    decrypted = DESEnctyption.des_decrypt(encrypted, key_copy)
    assert decrypted == text


if __name__ == '__main__':
    main()