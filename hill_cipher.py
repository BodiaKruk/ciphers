import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from collections import Counter

def preprocess_text(text, alphabet):
    return ''.join([char for char in text if char in alphabet])

def char_to_num(char):
    return used_alphabet.index(char)

def num_to_char(num):
    return used_alphabet[num % alphabet_length]

def plot_histogram(data, title, xlabel, ylabel):
    chars, counts = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.bar(chars, counts)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def find_ngrams(text, n):
    ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
    return Counter(ngrams)

def key_to_matrix(key, n):
    key_nums = [char_to_num(char) for char in key]
    if len(key_nums) != n * n:
        raise ValueError(f"Довжина ключа повинна бути {n * n} символів для матриці {n}x{n}.")
    return np.array(key_nums).reshape(n, n)

def hill_encrypt(plaintext, key_matrix):
    n = key_matrix.shape[0]
    while len(plaintext) % n != 0:
        plaintext += ' '
    blocks = [plaintext[i:i+n] for i in range(0, len(plaintext), n)]
    encrypted_text = ""
    for block in blocks:
        block_nums = [char_to_num(char) for char in block]
        encrypted_block = np.dot(block_nums, key_matrix) % alphabet_length
        encrypted_text += ''.join(num_to_char(num) for num in encrypted_block)
    return encrypted_text

def modinv(a, alphabet_length):
    for i in range(1, alphabet_length):
        if (a * i) % alphabet_length == 1:
            return i
    return None

def matrix_mod_inv(key_matrix, alphabet_length):
    det = round(np.linalg.det(key_matrix))
    det_inv = modinv(det, alphabet_length)
    if det_inv is None:
        return None
    matrix_inv = det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    matrix_mod_inv = matrix_inv % alphabet_length
    return matrix_mod_inv

def hill_decrypt(encrypted_text, inverse_matrix):
    print(f"Матриця по модулю 32:\n {inverse_matrix}")
    n = key_matrix.shape[0]
    blocks = [encrypted_text[i:i + n] for i in range(0, len(encrypted_text), n)]
    decrypted_text = ""
    for block in blocks:
        block_nums = [char_to_num(char) for char in block]
        decrypted_block = np.dot(block_nums, inverse_matrix) % alphabet_length
        decrypted_text += ''.join(num_to_char(num) for num in decrypted_block)
    return decrypted_text.strip()

def plot_double_histogram_sorted(char_count, char_count_encrypted, title, xlabel, ylabel):
    open_sorted = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
    encrypted_sorted = sorted(char_count_encrypted.items(), key=lambda x: x[1], reverse=True)
    common_chars = set([char for char, _ in open_sorted]) & set([char for char, _ in encrypted_sorted])
    open_sorted_filtered = [(char, freq) for char, freq in open_sorted if char in common_chars]
    encrypted_sorted_filtered = [(char, freq) for char, freq in encrypted_sorted if char in common_chars]
    labels = [char for char, _ in open_sorted_filtered]
    open_freq = [freq for _, freq in open_sorted_filtered]
    encrypted_freq = [freq for _, freq in encrypted_sorted_filtered]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width / 2, open_freq, width, label='Відкритий текст', color='b')
    ax.bar(x + width / 2, encrypted_freq, width, label='Зашифрований текст', color='r')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()
    fig.tight_layout()
    plt.show()

def main():
    global used_alphabet, alphabet_length, key_matrix  # Додаємо глобальні змінні
    filename = input("Введіть назву файлу (наприклад, 'file.txt'): ")
    try:
        with open(filename, encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        return

    print("\n File content:\n", file_content, "\n")

    used_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '.', ',', ';', '-', "'"]
    alphabet_length = len(used_alphabet)
    file_content = preprocess_text(file_content, used_alphabet)

    char_count = Counter(file_content)
    print("Використаний алфавіт:")
    print("".join(used_alphabet))
    print("\n")

    print("Частота повторення символів (в алфавітному порядку):")
    for char in sorted(char_count):
        print(f"'{char}': {char_count[char]} разів")

    sorted_by_frequency = char_count.most_common()
    print("\nЧастота повторення символів (по спаданню частоти):")
    for char, count in sorted_by_frequency:
        print(f"'{char}': {count} разів")

    plot_histogram(sorted(char_count.items()), "Гістограма (в алфавітному порядку)", "Символ", "Частота")
    plot_histogram(sorted_by_frequency, "Гістограма (по спаданню частоти)", "Символ", "Частота")

    bigrams = find_ngrams(file_content, 2)
    filtered_bigrams = bigrams.most_common(15)
    trigrams = find_ngrams(file_content, 3)
    filtered_trigrams = trigrams.most_common(15)
    fourgrams = find_ngrams(file_content, 4)
    filtered_fourgrams = fourgrams.most_common(15)

    plot_histogram(filtered_bigrams, "Гістограма біграм (15 найпоширеніших)", "Біграм", "Частота")
    plot_histogram(filtered_trigrams, "Гістограма триграм (15 найпоширеніших)", "Трьограм", "Частота")
    plot_histogram(filtered_fourgrams, "Гістограма чотириграм (15 найпоширеніших)", "Чотириграм", "Частота")

    print("\nПовторення біграм (15 найпоширеніших):")
    for bigram, count in filtered_bigrams:
        print(f"'{bigram}': {count} разів")

    print("\nПовторення триграм (15 найпоширеніших):")
    for trigram, count in filtered_trigrams:
        print(f"'{trigram}': {count} разів")

    print("\nПовторення чотириграм (15 найпоширеніших):")
    for fourgram, count in filtered_fourgrams:
        print(f"'{fourgram}': {count} разів")

    plaintext = file_content

    key = input("Введіть ключове слово для матриці шифрування: ").upper()
    matrix_size = int(np.sqrt(len(key)))
    key_matrix = key_to_matrix(key, matrix_size)

    print(f"\nКлючова матриця:\n{key_matrix}")

    print(f"\nТекст для шифрування: {plaintext}")
    encrypted_text = hill_encrypt(plaintext, key_matrix)
    print(f"\nЗашифрований текст: {encrypted_text}")

    inverse_matrix = matrix_mod_inv(key_matrix, alphabet_length)
    decrypted_text = hill_decrypt(encrypted_text, inverse_matrix)
    print(f"\nРозшифрований текст: {decrypted_text}")

    char_count_encrypted = Counter(encrypted_text)
    print("Частота повторення символів (в алфавітному порядку) ШТ:")
    for char in sorted(char_count_encrypted):
        print(f"'{char}': {char_count_encrypted[char]} разів")

    sorted_by_frequency_encrypted = char_count_encrypted.most_common()
    print("\nЧастота повторення символів (по спаданню частоти) ШТ:")
    for char, count in sorted_by_frequency_encrypted:  # Виправлено тут
        print(f"'{char}': {count} разів")

    plot_histogram(sorted(char_count_encrypted.items()), "Гістограма (в алфавітному порядку) ШТ", "Символ", "Частота")
    plot_histogram(sorted_by_frequency_encrypted, "Гістограма (по спаданню частоти) ШТ", "Символ", "Частота")

    bigrams_encrypted = find_ngrams(encrypted_text, 2)
    filtered_bigrams_encrypted = bigrams_encrypted.most_common(15)
    trigrams_encrypted = find_ngrams(encrypted_text, 3)
    filtered_trigrams_encrypted = trigrams_encrypted.most_common(15)
    fourgrams_encrypted = find_ngrams(encrypted_text, 4)
    filtered_fourgrams_encrypted = fourgrams_encrypted.most_common(15)

    plot_histogram(filtered_bigrams_encrypted, "Гістограма біграм (15 найпоширеніших) ШТ", "Біграм", "Частота")
    plot_histogram(filtered_trigrams_encrypted, "Гістограма триграм (15 найпоширеніших) ШТ", "Трьограм", "Частота")
    plot_histogram(filtered_fourgrams_encrypted, "Гістограма чотириграм (15 найпоширеніших) ШТ", "Чотириграм", "Частота")

    print("\nПовторення біграм (15 найпоширеніших) ШТ:")
    for bigram, count in filtered_bigrams_encrypted:
        print(f"'{bigram}': {count} разів")

    print("\nПовторення триграм (15 найпоширеніших) ШТ:")
    for trigram, count in filtered_trigrams_encrypted:
        print(f"'{trigram}': {count} разів")

    print("\nПовторення чотириграм (15 найпоширеніших) ШТ:")
    for fourgram, count in filtered_fourgrams_encrypted:
        print(f"'{fourgram}': {count} разів")

    plot_double_histogram_sorted(char_count, char_count_encrypted, "Порівняння частот символів (відсортовані за спаданням)", "Символи", "Частота")

if __name__ == "__main__":
    main()