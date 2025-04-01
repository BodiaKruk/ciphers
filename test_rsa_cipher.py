import unittest
from collections import Counter
from rsa_cipher import char_to_num
from rsa_cipher import num_to_char
from rsa_cipher import gcd
from rsa_cipher import mod_inverse
from rsa_cipher import generate_keys
from rsa_cipher import encrypt_block
from rsa_cipher import decrypt_block
from rsa_cipher import preprocess_text
from rsa_cipher import find_ngrams

class TestCharToNum(unittest.TestCase):
    def test_char_to_num(self):
        self.assertEqual(char_to_num('A'), 0)
        self.assertEqual(char_to_num(' '), 26)
        self.assertEqual(char_to_num('.'), 27)
    def test_num_to_char(self):
        self.assertEqual(num_to_char(0), 'A')
        self.assertEqual(num_to_char(26), ' ')
        self.assertEqual(num_to_char(27), '.')

    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(101, 103), 1)

    def test_mod_inverse(self):
        self.assertEqual(mod_inverse(3, 11), 4)
        self.assertEqual(mod_inverse(10, 17), 12)

    def test_generate_keys(self):
        public_key, private_key = generate_keys(89, 149)
        self.assertIsInstance(public_key, tuple)
        self.assertIsInstance(private_key, tuple)

    def test_encrypt_decrypt(self):
        p, q = 89, 149
        public_key, private_key = generate_keys(p, q)
        n, e = public_key
        _, d = private_key
        message = 123
        encrypted = encrypt_block(message, e, n)
        decrypted = decrypt_block(encrypted, d, n)
        self.assertEqual(message, decrypted)

    def test_preprocess_text(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,;-"
        text = "Hello, World!"  # Очікуємо "HELLO WORLD"
        self.assertEqual(preprocess_text(text.upper(), alphabet), "HELLO, WORLD")

    def test_find_ngrams(self):
        text = "ABABAB"
        bigrams = find_ngrams(text, 2)
        expected = Counter({"AB": 3, "BA": 2})
        self.assertEqual(bigrams, expected)




