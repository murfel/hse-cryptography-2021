from typing import List, Any


class Tools:
    @staticmethod
    def bool_list_to_binstring(text: List[bool]) -> str:
        return ''.join(list(map(lambda x: str(int(x)), text)))

    @staticmethod
    def flatten(arr: List[List[Any]]) -> List[Any]:
        return [item for sublist in arr for item in sublist]

    @staticmethod
    def int_to_bool_list(num: int, width=8) -> List[bool]:
        assert 0 <= num <= 2 ** width - 1
        return list(map(lambda x: bool(int(x)), format(num, '08b')))

    @staticmethod
    def bool_list_to_int(lst: List[bool]) -> int:
        return int(''.join(map(lambda x: str(int(x)), lst)), 2)

    @staticmethod
    def left_shift(arr: List[Any], num: int) -> List[Any]:
        shifted_arr = list(arr)
        for _ in range(num):
            shifted_arr.append(shifted_arr[0])
            shifted_arr.pop(0)
        return shifted_arr

    @staticmethod
    def left_shift_inplace(arr: List[Any], num: int):
        for _ in range(num):
            arr.append(arr[0])
            arr.pop(0)

    @staticmethod
    def right_shift_inplace(arr: List[Any], num: int):
        for _ in range(num):
            arr.insert(0, arr[-1])
            arr.pop()

    @staticmethod
    def xor(*args: List[bool]) -> List[bool]:
        from functools import reduce
        ans = [reduce(lambda x, y: x ^ y, tpl) for tpl in zip(*args)]
        return ans

    @staticmethod
    def ith_chunk(bits: List[bool], i: int, chunk_size: int) -> List[bool]:
        return bits[i * chunk_size:(i + 1) * chunk_size]

    @staticmethod
    def _flat_state_to_byte_state(state: List[Any], byte_size=8) -> List[List[Any]]:
        return [Tools.ith_chunk(state, i, byte_size) for i in range(len(state) // byte_size)]

    @staticmethod
    def _byte_state_to_column_first(state: List[Any], rows=4) -> List[List[Any]]:
        return [[state[i] for i in range(len(state)) if i % rows == row] for row in range(rows)]

    @staticmethod
    def flat_state_to_column_first(state: List[Any], byte_size=8, rows=4) -> List[List[Any]]:
        return Tools._byte_state_to_column_first(Tools._flat_state_to_byte_state(state, byte_size), rows)

    @staticmethod
    def _column_first_to_byte_state(table_state: List[List[Any]]) -> List[Any]:
        flat_state = []
        for col in range(len(table_state[0])):
            for row in range(len(table_state)):
                flat_state.append(table_state[row][col])
        return flat_state

    @staticmethod
    def column_first_to_flat_state(state: List[List[Any]]) -> List[Any]:
        return Tools.flatten(Tools._column_first_to_byte_state(state))


class AES:
    # https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
    # https://ru.wikipedia.org/wiki/Advanced_Encryption_Standard
    BYTE_SIZE_BITS = 8
    WORD_SIZE_BITS = 32
    BLOCK_SIZE_BITS = 128
    BLOCK_SIZE_BYTES = BLOCK_SIZE_BITS // BYTE_SIZE_BITS
    KEY_SIZE_BITS = 192
    NUM_ROUNDS = 12
    SBOXES = {0: 99, 1: 124, 2: 119, 3: 123, 4: 242, 5: 107, 6: 111, 7: 197, 8: 48, 9: 1, 10: 103, 11: 43, 12: 254, 13: 215, 14: 171, 15: 118, 16: 202, 17: 130, 18: 201, 19: 125, 20: 250, 21: 89, 22: 71, 23: 240, 24: 173, 25: 212, 26: 162, 27: 175, 28: 156, 29: 164, 30: 114, 31: 192, 32: 183, 33: 253, 34: 147, 35: 38, 36: 54, 37: 63, 38: 247, 39: 204, 40: 52, 41: 165, 42: 229, 43: 241, 44: 113, 45: 216, 46: 49, 47: 21, 48: 4, 49: 199, 50: 35, 51: 195, 52: 24, 53: 150, 54: 5, 55: 154, 56: 7, 57: 18, 58: 128, 59: 226, 60: 235, 61: 39, 62: 178, 63: 117, 64: 9, 65: 131, 66: 44, 67: 26, 68: 27, 69: 110, 70: 90, 71: 160, 72: 82, 73: 59, 74: 214, 75: 179, 76: 41, 77: 227, 78: 47, 79: 132, 80: 83, 81: 209, 82: 0, 83: 237, 84: 32, 85: 252, 86: 177, 87: 91, 88: 106, 89: 203, 90: 190, 91: 57, 92: 74, 93: 76, 94: 88, 95: 207, 96: 208, 97: 239, 98: 170, 99: 251, 100: 67, 101: 77, 102: 51, 103: 133, 104: 69, 105: 249, 106: 2, 107: 127, 108: 80, 109: 60, 110: 159, 111: 168, 112: 81, 113: 163, 114: 64, 115: 143, 116: 146, 117: 157, 118: 56, 119: 245, 120: 188, 121: 182, 122: 218, 123: 33, 124: 16, 125: 255, 126: 243, 127: 210, 128: 205, 129: 12, 130: 19, 131: 236, 132: 95, 133: 151, 134: 68, 135: 23, 136: 196, 137: 167, 138: 126, 139: 61, 140: 100, 141: 93, 142: 25, 143: 115, 144: 96, 145: 129, 146: 79, 147: 220, 148: 34, 149: 42, 150: 144, 151: 136, 152: 70, 153: 238, 154: 184, 155: 20, 156: 222, 157: 94, 158: 11, 159: 219, 160: 224, 161: 50, 162: 58, 163: 10, 164: 73, 165: 6, 166: 36, 167: 92, 168: 194, 169: 211, 170: 172, 171: 98, 172: 145, 173: 149, 174: 228, 175: 121, 176: 231, 177: 200, 178: 55, 179: 109, 180: 141, 181: 213, 182: 78, 183: 169, 184: 108, 185: 86, 186: 244, 187: 234, 188: 101, 189: 122, 190: 174, 191: 8, 192: 186, 193: 120, 194: 37, 195: 46, 196: 28, 197: 166, 198: 180, 199: 198, 200: 232, 201: 221, 202: 116, 203: 31, 204: 75, 205: 189, 206: 139, 207: 138, 208: 112, 209: 62, 210: 181, 211: 102, 212: 72, 213: 3, 214: 246, 215: 14, 216: 97, 217: 53, 218: 87, 219: 185, 220: 134, 221: 193, 222: 29, 223: 158, 224: 225, 225: 248, 226: 152, 227: 17, 228: 105, 229: 217, 230: 142, 231: 148, 232: 155, 233: 30, 234: 135, 235: 233, 236: 206, 237: 85, 238: 40, 239: 223, 240: 140, 241: 161, 242: 137, 243: 13, 244: 191, 245: 230, 246: 66, 247: 104, 248: 65, 249: 153, 250: 45, 251: 15, 252: 176, 253: 84, 254: 187, 255: 22}
    SBOXES_REV = {}
    RC = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
    RCON: List[List[bool]] = []

    byte = list[bool]

    for key, value in SBOXES.items():
        SBOXES_REV[value] = key

    for num in RC:
        RCON.append(Tools.int_to_bool_list(num) + [False for _ in range(32 - 8)])

    @staticmethod
    def _rot_word(word: List[bool], bits: int = 8) -> List[bool]:
        assert len(word) == AES.WORD_SIZE_BITS
        return Tools.left_shift(list(word), bits)

    @staticmethod
    def _apply_s_box(byte: byte) -> byte:
        assert len(byte) == AES.BYTE_SIZE_BITS
        return Tools.int_to_bool_list(AES.SBOXES[Tools.bool_list_to_int(byte)])

    @staticmethod
    def _apply_s_box_rev(byte: byte) -> byte:
        assert len(byte) == AES.BYTE_SIZE_BITS
        return Tools.int_to_bool_list(AES.SBOXES_REV[Tools.bool_list_to_int(byte)])

    @staticmethod
    def _sub_word(word: List[bool]) -> List[bool]:
        assert len(word) == AES.WORD_SIZE_BITS
        converted = [AES._apply_s_box(Tools.ith_chunk(word, i, AES.BYTE_SIZE_BITS)) for i in range(4)]
        return Tools.flatten(converted)

    @staticmethod
    def _generate_round_keys(key: List[bool]) -> List[List[bool]]:
        assert len(key) == AES.KEY_SIZE_BITS
        N = AES.KEY_SIZE_BITS // AES.WORD_SIZE_BITS  # key lengths in words
        keys_needed = AES.NUM_ROUNDS + 1
        flat_words = list(key)

        def ith_word(i: int) -> List[bool]:
            return Tools.ith_chunk(flat_words, i, AES.WORD_SIZE_BITS)

        for i in range(N, 4 * keys_needed):
            if i % N == 0:
                word = Tools.xor(ith_word(i - N),
                                 AES._sub_word(AES._rot_word(ith_word(i - 1))),
                                 AES.RCON[i // N])
            elif i > 6 and i % N == 4:
                word = Tools.xor(ith_word(i - N),
                                 AES._sub_word(ith_word(i - 1)))
            else:
                word = Tools.xor(ith_word(i - N),
                                 ith_word(i - 1))
            assert len(word) == 32
            flat_words.extend(word)
        round_keys = [flat_words[i * AES.BLOCK_SIZE_BITS:(i + 1) * AES.BLOCK_SIZE_BITS]
                      for i in range(keys_needed)]
        return round_keys

    @staticmethod
    def _add_round_key(state: List[List[byte]], prev_round_key: List[List[byte]]):
        for row in range(len(state)):
            for col in range(len(state[0])):
                state[row][col] = Tools.xor(state[row][col], prev_round_key[row][col])

    @staticmethod
    def _sub_bytes(state: List[List[byte]]):
        for row in range(len(state)):
            for col in range(len(state[0])):
                state[row][col] = AES._apply_s_box(state[row][col])

    @staticmethod
    def _inv_sub_bytes(state: List[List[byte]]):
        for row in range(len(state)):
            for col in range(len(state[0])):
                state[row][col] = AES._apply_s_box_rev(state[row][col])

    @staticmethod
    def _shift_rows(state: List[List[byte]]):
        for i, row in enumerate(state):
            Tools.left_shift_inplace(row, i)

    @staticmethod
    def _inv_shift_rows(state: List[List[byte]]):
        for i, row in enumerate(state):
            Tools.right_shift_inplace(row, i)

    @staticmethod
    def _mix_columns(state: List[List[byte]]):
        pass

    @staticmethod
    def _inv_mix_columns(state: List[List[byte]]):
        pass

    @staticmethod
    def encrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == AES.BLOCK_SIZE_BITS
        assert len(key) == AES.KEY_SIZE_BITS

        round_keys_raw = AES._generate_round_keys(key)
        round_keys = [Tools.flat_state_to_column_first(round_key) for round_key in round_keys_raw]

        state = list(text)
        state = Tools.flat_state_to_column_first(state)

        AES._add_round_key(state, round_keys[0])

        for round_num in range(1, AES.NUM_ROUNDS - 1):
            AES._sub_bytes(state)
            AES._shift_rows(state)
            AES._mix_columns(state)
            AES._add_round_key(state, round_keys[round_num])

        AES._sub_bytes(state)
        AES._shift_rows(state)
        AES._add_round_key(state, round_keys[-1])

        return Tools.column_first_to_flat_state(state)

    @staticmethod
    def decrypt(text: List[bool], key: List[bool]) -> List[bool]:
        assert len(text) == AES.BLOCK_SIZE_BITS
        assert len(key) == AES.KEY_SIZE_BITS

        round_keys_raw = AES._generate_round_keys(key)
        round_keys = [Tools.flat_state_to_column_first(round_key) for round_key in round_keys_raw]

        state = list(text)
        state = Tools.flat_state_to_column_first(state)

        AES._add_round_key(state, round_keys[-1])

        for round_num in reversed(range(1, AES.NUM_ROUNDS - 1)):
            AES._inv_shift_rows(state)
            AES._inv_sub_bytes(state)
            AES._add_round_key(state, round_keys[round_num])
            AES._inv_mix_columns(state)

        AES._inv_shift_rows(state)
        AES._inv_sub_bytes(state)
        AES._add_round_key(state, round_keys[0])

        return Tools.column_first_to_flat_state(state)


def main():
    from random import randint
    text = [bool(randint(0, 1)) for _ in range(AES.BLOCK_SIZE_BITS)]
    key = [bool(randint(0, 1)) for _ in range(AES.KEY_SIZE_BITS)]
    key_copy = list(key)
    encrypted = AES.encrypt(text, key)
    # print(text)
    # print(encrypted)
    decrypted = AES.decrypt(encrypted, key_copy)
    assert decrypted == text


if __name__ == '__main__':
    main()
