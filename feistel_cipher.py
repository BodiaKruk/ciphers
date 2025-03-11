import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' if you don't need interactive plots
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

def feistel_encrypt_block(L, R, key, rounds=11):
    """Шифрування блоку тексту (два символи) методом Фейстеля"""
    def F(R, key):
        return R ^ key  # Проста функція XOR
    for i in range(rounds):
        old_R = R
        R = L ^ F(R, key)
        L = old_R
        key += 1
    return L, R

def feistel_encrypt_text(file_content, key, rounds=11):
    """Шифрування всього тексту методом Фейстеля"""
    encrypted_text = []
    for i in range(0, len(file_content), 2):
        if i + 1 < len(file_content):
            L, R = ord(file_content[i]), ord(file_content[i + 1])
        else:
            L, R = ord(file_content[i]), ord(' ')
        L_enc, R_enc = feistel_encrypt_block(L, R, key, rounds)
        encrypted_text.append(chr(L_enc))
        encrypted_text.append(chr(R_enc))
    return ''.join(encrypted_text)

def feistel_decrypt_block(L, R, key, rounds=11):
    """Розшифрування блоку тексту (два символи) методом Фейстеля"""
    def F(R, key):
        return R ^ key  # Проста функція XOR
    for i in range(rounds):
        old_L = L
        L = R ^ F(L, key)
        R = old_L
        key -= 1
    return L, R

def feistel_decrypt_text(encrypted_text, key, rounds=11):
    """Розшифрування всього тексту методом Фейстеля"""
    decrypted_text = []
    for i in range(0, len(encrypted_text), 2):
        if i + 1 < len(encrypted_text):
            L, R = ord(encrypted_text[i]), ord(encrypted_text[i + 1])
        else:
            L, R = ord(encrypted_text[i]), ord(' ')
        L_dec, R_dec = feistel_decrypt_block(L, R, key + rounds - 1, rounds)
        decrypted_text.append(chr(L_dec))
        decrypted_text.append(chr(R_dec))
    return ''.join(decrypted_text)

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
    global used_alphabet, alphabet_length
    # Зчитування файлу
    filename = input("Введіть назву фай óлу (наприклад, 'file.txt'): ")
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

    # Визначення алфавіту
    used_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '.', ',', ';', '-', "'"]
    alphabet_length = len(used_alphabet)
    file_content = preprocess_text(file_content, used_alphabet)

    # Підрахунок частоти символів ВТ
    char_count = Counter(file_content)

    print("Використаний алфавіт:")
    print("".join(used_alphabet))
    print("\n")

    # Частота повторення символів (в алфавітному порядку)
    print("Частота повторення символів (в алфавітному порядку):")
    for char in sorted(char_count):
        print(f"'{char}': {char_count[char]} разів")

    sorted_by_frequency = char_count.most_common()
    print("\nЧастота повторення символів (по спаданню частоти):")
    for char, count in sorted_by_frequency:
        print(f"'{char}': {count} разів")

    # Гістограми частоти символів
    plot_histogram(sorted(char_count.items()), "Гістограма (в алфавітному порядку)", "Символ", "Частота")
    plot_histogram(sorted_by_frequency, "Гістограма (по спаданню частоти)", "Символ", "Частота")

    # Підрахунок біграмів, тріграмів та чотириграмів
    bigrams = find_ngrams(file_content, 2)
    filtered_bigrams = bigrams.most_common(15)
    trigrams = find_ngrams(file_content, 3)
    filtered_trigrams = trigrams.most_common(15)
    fourgrams = find_ngrams(file_content, 4)
    filtered_fourgrams = fourgrams.most_common(15)

    # Гістограми n-грамів
    plot_histogram(filtered_bigrams, "Гістограма біграм (15 найпоширеніших)", "Біграм", "Частота")
    plot_histogram(filtered_trigrams, "Гістограма триграм (15 найпоширеніших)", "Трьограм", "Частота")
    plot_histogram(filtered_fourgrams, "Гістограма чотириграм (15 найпоширеніших)", "Чотириграм", "Частота")

    # Виведення повторень n-грамів
    print("\nПовторення біграм (15 найпоширеніших):")
    for bigram, count in filtered_bigrams:
        print(f"'{bigram}': {count} разів")

    print("\nПовторення триграм (15 найпоширеніших):")
    for trigram, count in filtered_trigrams:
        print(f"'{trigram}': {count} разів")

    print("\nПовторення чотириграм (15 найпоширеніших):")
    for fourgram, count in filtered_fourgrams:
        print(f"'{fourgram}': {count} разів")

    # Початковий ключ
    key = 10

    # Шифрування тексту
    encrypted_text = feistel_encrypt_text(file_content, key)
    print(f"\nЗашифрований текст:\n{encrypted_text}")

    # Підрахунок частоти символів у зашифрованому тексті
    char_count_encrypted = Counter(encrypted_text)
    encrypted_content = preprocess_text(encrypted_text, used_alphabet)
    encrypted_char_count = Counter(encrypted_content)

    # Виведення частоти повторення символів у зашифрованому тексті
    print("\nЧастота повторення символів у зашифрованому тексті (в алфавітному порядку):")
    for char in sorted(encrypted_char_count):
        print(f"'{char}': {encrypted_char_count[char]} разів")

    sorted_by_frequency_enc = encrypted_char_count.most_common()
    print("\nЧастота повторення символів у зашифрованому тексті (по спаданню частоти):")
    for char, count in sorted_by_frequency_enc:
        print(f"'{char}': {count} разів")

    # Гістограми для зашифрованого тексту
    plot_histogram(sorted(encrypted_char_count.items()), "Гістограма (в алфавітному порядку, зашифрований текст)", "Символ", "Частота")
    plot_histogram(sorted_by_frequency_enc, "Гістограма (по спаданню частоти, зашифрований текст)", "Символ", "Частота")

    # Підрахунок n-грамів у зашифрованому тексті
    encrypted_bigrams = find_ngrams(encrypted_content, 2)
    filtered_encrypted_bigrams = encrypted_bigrams.most_common(15)
    encrypted_trigrams = find_ngrams(encrypted_content, 3)
    filtered_encrypted_trigrams = encrypted_trigrams.most_common(15)
    encrypted_fourgrams = find_ngrams(encrypted_content, 4)
    filtered_encrypted_fourgrams = encrypted_fourgrams.most_common(15)

    # Гістограми n-грамів для зашифрованого тексту
    plot_histogram(filtered_encrypted_bigrams, "Гістограма біграм (зашифрований текст)", "Біграм", "Частота")
    plot_histogram(filtered_encrypted_trigrams, "Гістограма триграм (зашифрований текст)", "Триграм", "Частота")
    plot_histogram(filtered_encrypted_fourgrams, "Гістограма чотириграм (зашифрований текст)", "Чотириграм", "Частота")

    # Виведення повторень n-грамів у зашифрованому тексті
    print("\nПовторення біграм (зашифрований текст, 15 найпоширеніших):")
    for bigram, count in filtered_encrypted_bigrams:
        print(f"'{bigram}': {count} разів")

    print("\nПовторення триграм (зашифрований текст, 15 найпоширеніших):")
    for trigram, count in filtered_encrypted_trigrams:
        print(f"'{trigram}': {count} разів")

    print("\nПовторення чотириграм (зашифрований текст, 15 найпоширеніших):")
    for fourgram, count in filtered_encrypted_fourgrams:
        print(f"'{fourgram}': {count} разів")

    # Розшифрування тексту
    decrypted_text = feistel_decrypt_text(encrypted_text, key)
    print(f"\nРозшифрований текст:\n{decrypted_text}")

    # Порівняльна гістограма
    plot_double_histogram_sorted(char_count, char_count_encrypted, "Порівняння частот символів (відсортовані за спаданням)", "Символи", "Частота")

if __name__ == "__main__":
    main()