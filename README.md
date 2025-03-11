Program is a console utility for encrypting texts from files using various cryptographic algorithms. It consists of the main file main.py and four encryption modules: hill_cipher.py, feistel_cipher.py, vigener_cipher.py, and rsa_cipher.py. Here is a detailed description:

General program description.
Purpose: Encrypt and analyze text from a file using four algorithms: Hill cipher, Feistel cipher, Vigener cipher, and RSA.
Interface: Console, the user interacts through keyboard input.
Functionality:
Selecting an encryption algorithm.
Entering the name of the file with the text to be encrypted.
Encrypting the text using the selected algorithm.
Analyzing the frequency of characters and n-grams (bigrams, trigrams, quadrams) in plaintext and encrypted text.
Decryption of the text (where applicable).
Visualization of the results through histograms using Matplotlib.
