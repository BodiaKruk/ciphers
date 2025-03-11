import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' if you don't need interactive plots
import matplotlib.pyplot as plt
from collections import Counter

def preprocess_text(text, alphabet):
    return ''.join([char for char in text if char in alphabet])

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

def create_vigenere_table(alphabet):
    size = len(alphabet)
    vigener_table = np.empty((size, size), dtype=str)
    for i in range(size):
        for j in range(size):
            vigener_table[i, j] = alphabet[(i + j) % size]
    return vigener_table

def encrypt(text, key, vigener_table, alphabet):
    result = []
    for i in range(len(text)):
        x = alphabet.index(text[i])
        y = alphabet.index(key[i % len(key)])
        result.append(vigener_table[x, y])
    return ''.join(result)

def decrypt(text, key, vigener_table, alphabet):
    result = []
    for i in range(len(text)):
        y = alphabet.index(key[i % len(key)])
        vector = [vigener_table[j, y] for j in range(len(alphabet))]
        x = vector.index(text[i])
        result.append(alphabet[x])
    return ''.join(result)

def plot_double_histogram_sorted(open_char_count, cipher_char_count, title, xlabel, ylabel):
    open_sorted = sorted(open_char_count.items(), key=lambda x: x[1], reverse=True)
    cipher_sorted = sorted(cipher_char_count.items(), key=lambda x: x[1], reverse=True)
    common_chars = set([char for char, _ in open_sorted]) & set([char for char, _ in cipher_sorted])
    open_sorted_filtered = [(char, freq) for char, freq in open_sorted if char in common_chars]
    cipher_sorted_filtered = [(char, freq) for char, freq in cipher_sorted if char in common_chars]
    labels = [char for char, _ in open_sorted_filtered]
    open_freq = [freq for _, freq in open_sorted_filtered]
    cipher_freq = [freq for _, freq in cipher_sorted_filtered]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width / 2, open_freq, width, label='Відкритий текст', color='b')
    ax.bar(x + width / 2, cipher_freq, width, label='Зашифрований текст', color='r')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()
    fig.tight_layout()
    plt.show()

def main():
    global used_alphabet
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
    file_content = preprocess_text(file_content, used_alphabet)

    # Підрахунок частоти символів
    char_count = Counter(file_content)
    print("Використаний алфавіт:")
    print("".join(used_alphabet))
    print("\n")
    print(file_content, "\n")

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

    # Введення ключа
    key = str(input("\nВведіть ключ для шифру Віженера: "))

    # Створення таблиці Віженера
    vigener_table = create_vigenere_table(used_alphabet)

    # Шифрування та розшифрування
    ciphertext = encrypt(file_content, key, vigener_table, used_alphabet)
    decrypted_text = decrypt(ciphertext, key, vigener_table, used_alphabet)

    print("\nЗашифрований текст:\n", ciphertext)
    print("Розшифрований текст:\n", decrypted_text)

    # Аналіз зашифрованого тексту
    char1_count = Counter(ciphertext)
    print("Використаний алфавіт:")
    print("".join(used_alphabet))
    print("\n")

    # Частота повторення символів (в алфавітному порядку)
    print("Частота повторення символів (в алфавітному порядку):")
    for char in sorted(char1_count):
        print(f"'{char}': {char1_count[char]} разів")

    sorted_by_frequency = char1_count.most_common()
    print("\nЧастота повторення символів (по спаданню частоти):")
    for char, count in sorted_by_frequency:
        print(f"'{char}': {count} разів")

    # Гістограми частоти символів
    plot_histogram(sorted(char1_count.items()), "Гістограма (в алфавітному порядку)", "Символ", "Частота")
    plot_histogram(sorted_by_frequency, "Гістограма (по спаданню частоти)", "Символ", "Частота")

    # Підрахунок n-грамів у зашифрованому тексті
    bigrams = find_ngrams(ciphertext, 2)
    filtered_bigrams = bigrams.most_common(15)
    trigrams = find_ngrams(ciphertext, 3)
    filtered_trigrams = trigrams.most_common(15)
    fourgrams = find_ngrams(ciphertext, 4)
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

    # Порівняльна гістограма
    char_count_open = Counter(file_content)
    char_count_cipher = Counter(ciphertext)
    plot_double_histogram_sorted(char_count_open, char_count_cipher, "Порівняння частот символів (відсортовані за спаданням)", "Символи", "Частота")

if __name__ == "__main__":
    main()