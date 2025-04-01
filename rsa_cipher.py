import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' if you don't need interactive plots
import matplotlib.pyplot as plt
from collections import Counter
import random

used_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,;-"  # або ваш алфавіт
alphabet_length = len(used_alphabet)

# Функція для попередньої обробки тексту
def preprocess_text(text, alphabet):
    return ''.join([char for char in text if char in alphabet])

# Функція для перетворення символу на число
def char_to_num(char):
    return used_alphabet.index(char)

# Функція для перетворення числа на символ
def num_to_char(num):
    return used_alphabet[num % alphabet_length]

# Функція для побудови гістограми
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

# Функція для знаходження n-грамів
def find_ngrams(text, n):
    ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
    return Counter(ngrams)

# Функція для обчислення найбільшого спільного дільника (GCD)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Функція для обчислення оберненого значення за модулем
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Функція для генерації ключів RSA
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.choice([i for i in range(2, phi) if gcd(i, phi) == 1])
    e = 10965  # Фіксоване значення для прикладу
    d = mod_inverse(e, phi)
    return (n, e), (n, d)

# Функція шифрування RSA
def encrypt_block(block, e, n):
    return pow(block, e, n)

# Функція розшифрування RSA
def decrypt_block(encrypted_block, d, n):
    return pow(encrypted_block, d, n)

# Перетворення зашифрованих чисел у символи ASCII
def encrypted_blocks_to_text(encrypted_blocks):
    return ''.join(chr(block) for block in encrypted_blocks)

# Перетворення розшифрованих чисел у символи ASCII з відновленням початкового тексту
def decrypted_blocks_to_text(decrypted_blocks):
    chars = []
    for block in decrypted_blocks:
        first_char_code = block // 10
        second_char_code = (block % 10) * 10
        chars.append(chr(first_char_code))
        if second_char_code < 128:
            chars.append(chr(second_char_code))
    return ''.join(chars)

# Функція для побудови комбінованого графіка частоти символів
def plot_combined_histogram(original_data, encrypted_data):
    chars_orig, counts_orig = zip(*original_data)
    chars_enc, counts_enc = zip(*encrypted_data)
    max_count = max(max(counts_orig), max(counts_enc))
    plt.figure(figsize=(10, 6))
    plt.bar(chars_orig, counts_orig, alpha=0.5, label='Оригінальний текст', color='blue', width=0.4, align='center')
    plt.bar(chars_enc, counts_enc, alpha=0.5, label='Зашифрований текст', color='red', width=0.4, align='edge')
    plt.title("Частота символів у оригінальному та зашифрованому текстах")
    plt.xlabel("Символ")
    plt.ylabel("Частота")
    plt.xticks(rotation=90)
    plt.ylim(0, max_count)
    plt.legend()
    plt.tight_layout()
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
    used_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ .,;-")
    alphabet_length = len(used_alphabet)
    file_content = preprocess_text(file_content, used_alphabet)

    # Підрахунок частоти символів
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
    bigrams = find_ngrams(file_content, 2).most_common(15)
    trigrams = find_ngrams(file_content, 3).most_common(15)
    fourgrams = find_ngrams(file_content, 4).most_common(15)

    # Гістограми n-грамів
    plot_histogram(bigrams, "Гістограма біграм (15 найпоширеніших)", "Біграм", "Частота")
    plot_histogram(trigrams, "Гістограма триграм (15 найпоширеніших)", "Триграм", "Частота")
    plot_histogram(fourgrams, "Гістограма чотириграм (15 найпоширеніших)", "Чотириграм", "Частота")

    # Перетворимо символи в числові коди за таблицею ASCII
    ascii_codes = [ord(char) for char in file_content]
    all_digits = ''.join(map(str, ascii_codes))  # Об'єднуємо всі числа в одну строку
    blocks1 = [all_digits[i:i + 3] for i in range(0, len(all_digits), 3)]  # Розбиваємо по 3 символи
    blocks = [int(block) for block in blocks1]  # Перетворення блоків у числа

    print(f"Текст для шифрування: {file_content}")
    print("ASCII-коди:", ascii_codes)
    print("Блоки по 1.5 символа:", blocks1)

    # Генерація ключів
    p, q = 89, 149
    public_key, private_key = generate_keys(p, q)
    n, e = public_key
    _, d = private_key

    print("\nPublic key:", public_key)
    print("Private key:", private_key)

    # Шифруємо кожен блок
    encrypted_blocks = [encrypt_block(block, e, n) for block in blocks]
    print("\nЗашифрований текст (цифри): ", encrypted_blocks)
    encrypted_text = encrypted_blocks_to_text(encrypted_blocks)
    print("\nЗашифрований текст (ASCII символи): ", encrypted_text)

    # Розшифровуємо кожен блок
    decrypted_blocks = [decrypt_block(enc_block, d, n) for enc_block in encrypted_blocks]
    print("\nРозшифрований текст (цифри): ", decrypted_blocks)
    decrypted_text = decrypted_blocks_to_text(decrypted_blocks)
    print("\nРозшифрований текст (ASCII символи): ", decrypted_text)  # Виправлено на decrypted_text

    # Аналіз зашифрованого тексту
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

    # Комбінована гістограма
    plot_combined_histogram(sorted_by_frequency, sorted_by_frequency_enc)

    # Підрахунок n-грамів у зашифрованому тексті
    encrypted_bigrams = find_ngrams(encrypted_content, 2).most_common(15)
    encrypted_trigrams = find_ngrams(encrypted_content, 3).most_common(15)
    encrypted_fourgrams = find_ngrams(encrypted_content, 4).most_common(15)

    # Гістограми n-грамів для зашифрованого тексту
    plot_histogram(encrypted_bigrams, "Гістограма біграм (зашифрований текст)", "Біграм", "Частота")
    plot_histogram(encrypted_trigrams, "Гістограма триграм (зашифрований текст)", "Триграм", "Частота")
    plot_histogram(encrypted_fourgrams, "Гістограма чотириграм (зашифрований текст)", "Чотириграм", "Частота")

    # Виведення повторень n-грамів у зашифрованому тексті
    print("\nПовторення біграм (зашифрований текст, 15 найпоширеніших):")
    for bigram, count in encrypted_bigrams:
        print(f"'{bigram}': {count} разів")

    print("\nПовторення триграм (зашифрований текст, 15 найпоширеніших):")
    for trigram, count in encrypted_trigrams:
        print(f"'{trigram}': {count} разів")

    print("\nПовторення чотириграм (зашифрований текст, 15 найпоширеніших):")
    for fourgram, count in encrypted_fourgrams:
        print(f"'{fourgram}': {count} разів")

if __name__ == "__main__":
    main()
