from collections import Counter

import vigenere

long_text = """
Before time was time, there was a Great Hill. 
And on the Great Hill there lived the Yolks.
The Yolks spent their entire lives climbing the Great Hill, trying to reach the top.
Some Yolks climbed fast.
Some Yolks climbed slowly.
One Yolk in particular was a very slow climber. He was different than the rest of the Yolks.
When he climbed, all the other Yolks passed him. 
It was hard for him to watch them pass by.
He felt like the worst climber in the world.
Some Yolks made fun of him as they passed.
Others didn’t.
Some Yolks wanted to help him climb but he didn’t let them.
It was hard for him to climb. It was even harder when it rained because the ground got slippery. Sometimes it seemed like it was only raining on him. 
But it wasn’t.
There were times when he felt like he wasn’t moving at all. 
But he was.
Then one day he met another Yolk who climbed even slower than he did.
He helped the slower Yolk climb.
“Thank You,” said the slower Yolk.
“You’re Welcome,” said the slow Yolk, “I can’t be of much help to anyone else since I climb so slowly.”
Slowly? asked the slower Yolk.
Well yes. I watch other Yolks pass me all the time.
I do not know if you are slow or fast, but I do know that you helped me, and that you are still climbing.
The slow Yolk said goodbye to the slower Yolk, and kept climbing. 
Still climbing, he thought to himself. 
That is true.
And he smiled.
So the Yolk kept climbing. He climbed when it was nice out, he climbed when it rained, and he even climbed when it snowed.
As he kept climbing he got better and better. 
Sometimes he would pass other Yolks and sometimes they would pass him. 
He had stopped paying attention. 
He also noticed that some Yolks were no longer climbing. 
When a yolk stops climbing it stays where it is. 
Some Yolks stop climbing because they are happy with how far they have gone. 
Others stop climbing because they don’t want to climb anymore. 
The Yolks that had stopped climbing did not like to be passed, and they made it harder to get by. 
But the Yolk kept climbing, right over them!
There were still times when the Yolk thought he was climbing an impossible hill, but he kept climbing. 
Always, always, climbing.
Do you think he made the top?
"""


def test_encrypt():
    assert vigenere.encrypt('attackatdawn', 'lemon') == 'lxfopvefrnhr'


def test_decrypt():
    assert vigenere.decrypt('lxfopvefrnhr', 'lemon') == 'attackatdawn'


def test_guess_key_length():
    key_lengths = vigenere.guess_key_lens('vhvsspqucemrvbvbbbvhvsurqgibdugrnicjqucervuaxssr')
    assert len(key_lengths) == 1
    assert key_lengths[0] == 6


def test_count_ngrams():
    print(vigenere.count_ngrams('hello', 2))


def test_ith_letters():
    assert vigenere.nth_letters('abcdefgh', 2) == 'aceg'


def clean_text(text: str):
    text = text.lower()
    text = [l for l in text if l.isalpha()]
    return ''.join(text)


def test_calc_letter_dist():
    dist = vigenere.calc_letter_dist('aaa')
    assert dist == {'a': 1}
    dist = vigenere.calc_letter_dist('aaabb')
    assert dist == {'a': 0.6, 'b': 0.4}


def test_dist_match_score_trivial():
    score = vigenere.dist_match_score(vigenere.english_letter_distribution, vigenere.english_letter_distribution)
    assert score == 0


def test_dist_match_score_harder():
    modified = dict(vigenere.english_letter_distribution)
    modified['a'] = 0
    score = vigenere.dist_match_score(vigenere.english_letter_distribution, modified)
    assert score == vigenere.english_letter_distribution['a'] ** 2


def test_dist_match_score():
    dist1 = vigenere.calc_letter_dist('ewinfeowobgreo')
    score1 = vigenere.dist_match_score(vigenere.english_letter_distribution, dist1)
    dist2 = vigenere.calc_letter_dist('hello there my name is potato')
    score2 = vigenere.dist_match_score(vigenere.english_letter_distribution, dist2)
    assert score1 > score2


def test_shift_and_encrypt():
    text = 'abcdefg'
    for i in range(26):
        letter = chr(ord('a') + i)
        assert vigenere.shift_text(text, letter) == vigenere.encrypt(text, letter)


def encrypt_decrtypt():
    text = 'abcdefg'
    assert text == vigenere.decrypt(vigenere.encrypt(text, 'b'), 'b')


def test():
    text = 'hello there my name is potato'
    text = clean_text(text)
    key = 'c'
    cyphertext = vigenere.encrypt(text, key)
    guessed_keys = vigenere.kasiski_test(cyphertext, len(key))
    assert guessed_keys[0] == key

    text = clean_text(long_text)
    key = 'andrew'
    cyphertext = vigenere.encrypt(text, key)
    guessed_keys = vigenere.kasiski_test(cyphertext, len(key))
    assert guessed_keys[0] == key