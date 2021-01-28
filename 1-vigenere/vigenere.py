from collections import defaultdict
from functools import reduce
from math import gcd
from typing import List, Tuple, Dict

from scipy.stats import chisquare

english_letter_distribution = {'e': 0.12,
                               't': 0.091,
                               'a': 0.0812,
                               'o': 0.0768,
                               'i': 0.0731,
                               'n': 0.0695,
                               's': 0.06280000000000001,
                               'r': 0.0602,
                               'h': 0.0592,
                               'd': 0.0432,
                               'l': 0.0398,
                               'u': 0.0288,
                               'c': 0.0271,
                               'm': 0.026099999999999998,
                               'f': 0.023,
                               'y': 0.021099999999999997,
                               'w': 0.0209,
                               'g': 0.0203,
                               'p': 0.0182,
                               'b': 0.0149,
                               'v': 0.0111,
                               'k': 0.0069,
                               'x': 0.0017000000000000001,
                               'q': 0.0011,
                               'j': 0.001,
                               'z': 0.0007000000000000001}


def validate_alpha_str(text: str):
    is_valid = all(letter.isalpha() for letter in text)
    if not is_valid:
        raise Exception('malformed input')


def validate_letter(letter: str):
    is_valid = letter.isalpha() and len(letter) == 1
    if not is_valid:
        raise Exception('not a letter')


def letter_sum(l1: str, l2: str, plus=True) -> str:
    validate_letter(l1)
    validate_letter(l2)
    return chr((ord(l1) - ord('a') + (1 if plus else -1) * (ord(l2) - ord('a'))) % 26 + ord('a'))


def encrypt(text: str, key: str) -> str:
    validate_alpha_str(text)
    validate_alpha_str(key)
    text.lower()
    key.lower()
    return ''.join(letter_sum(text[i], key[i % len(key)]) for i in range(len(text)))


def decrypt(text: str, key: str) -> str:
    validate_alpha_str(text)
    validate_alpha_str(key)
    text.lower()
    key.lower()
    return ''.join(letter_sum(text[i], key[i % len(key)], False) for i in range(len(text)))


def count_ngrams(text: str, n: int) -> List[Tuple[str, List[int]]]:
    ngram_to_cnt = defaultdict(list)
    for i in range(len(text) - n + 1):
        ngram_to_cnt[text[i:i + n]].append(i)
    lst = ngram_to_cnt.items()
    return sorted(lst, key=lambda t: len(t[1]), reverse=True)


def gcd_multiple(numbers: List[int]) -> int:
    return reduce(gcd, numbers, numbers[0])


def guess_key_lens(text: str) -> List[int]:
    key_lengths = []
    for n in range(3, 10):
        ngrams = count_ngrams(text, n)
        ngrams = list(filter(lambda ngram: len(ngram[1]) > 1, ngrams))
        dists = [abs(ngram[1][0] - ngram[1][1]) for ngram in ngrams]  # TODO: it only checks the first dist
        if len(dists) == 0:
            continue
        key_lengths.append(gcd_multiple(dists))  # TODO: might be a gcd divisor as well
    return list(set(key_lengths))


def dist_match_score(true_dist: Dict[str, float], dist: Dict[str, float], text_len) -> int:
    true_dist_arr = []
    dist_arr = []
    for key in true_dist.keys():
        true_dist_arr.append(true_dist[key] * text_len)
        dist_arr.append(dist[key])
    chisq, p = chisquare(dist_arr, true_dist_arr)
    print(chisq, p)
    return -p
    # error = 0
    # total = float(len(text))
    # for key in dist.keys():
    #     dist[key] /= total
    # for key in true_dist.keys():
    #     error += (true_dist[key] - dist[key]) ** 2
    # return error


def calc_letter_dist(text: str) -> Dict[str, float]:
    from collections import Counter
    dist = Counter(text)
    return dist


def shift_text(text: str, key: str):
    return ''.join(map(lambda letter: letter_sum(letter, key, False), text))


def guess_one_letter_key(text: str) -> str:
    key_to_score = dict()
    for i in range(26):
        letter = chr(ord('a') + i)
        shifted_text = shift_text(text, letter)
        dists = calc_letter_dist(shifted_text)
        key_to_score[letter] = dist_match_score(english_letter_distribution, dists, len(text))
    keys = key_to_score.items()
    keys = sorted(keys, key=lambda x: x[1])
    print(keys[:3])
    return keys[0][0]


def kasiski_test(text: str, key_length=None):
    if key_length is None:
        key_lens = guess_key_lens(text)
    else:
        key_lens = [key_length]
    keys = []
    for key_len in key_lens:
        key = []
        for i in range(key_len):
            key_letter = guess_one_letter_key(text[i::key_len])
            key.append(key_letter)
        keys.append(key)
    keys = [''.join(key) for key in keys]
    for key in keys:
        decr = decrypt(text, key)
        print(key, decr)
    return keys
