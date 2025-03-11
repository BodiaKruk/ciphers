import matplotlib.pyplot as plt
from collections import Counter

# Зчитування файлу
with open('СС_144.txt', encoding='utf-8') as file:
    file_content = file.read()

# Визначення алфавіту
used_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '.', ',', ';', '-', "'"]

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

# Гістограми частоти символів
plot_histogram(sorted(char_count.items()), "Гістограма (в алфавітному порядку)", "Символ", "Частота")
plot_histogram(sorted_by_frequency, "Гістограма (по спаданню частоти)", "Символ", "Частота")

# Функція для знаходження n-грамів
def find_ngrams(text, n):
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    return Counter(ngrams)

# Підрахунок біграмів, тріграмів та чотириграмів
bigrams = find_ngrams(file_content, 2)
filtered_bigrams = bigrams.most_common(15)  # Тільки 15 найпоширеніших

trigrams = find_ngrams(file_content, 3)
filtered_trigrams = trigrams.most_common(15)  # Тільки 15 найпоширеніших

fourgrams = find_ngrams(file_content, 4)
filtered_fourgrams = fourgrams.most_common(15)  # Тільки 15 найпоширеніших

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

# Обчислення зсуву для шифру Цезаря
most_common_char, most_common_count = sorted_by_frequency[0]  # Найбільш уживаний символ
space_position = used_alphabet.index(' ')  # Позиція пробілу в алфавіті
shift = (space_position - used_alphabet.index(most_common_char)) % len(used_alphabet)

# Функція для шифру Цезаря
def caesar_cipher(file_content, shift):
    decoded_text = []
    for char in file_content:
        if char in used_alphabet:
            index = used_alphabet.index(char)
            new_index = (index + shift) % len(used_alphabet)
            decoded_text.append(used_alphabet[new_index])
        else:
            decoded_text.append(char)
    return ''.join(decoded_text)

# Шифрування тексту
decoded_text = caesar_cipher(file_content, shift)

print("\nЗсув:")
print(shift)

print("\nDecoded text with Caesar cipher:")
print(decoded_text)

# Аналіз розшифрованого тексту
print("\nАналіз розшифрованого текстy:")
decoded_char_count = Counter(decoded_text)

print("\nЧастота повторення символів (в алфітному порядку):")
for char in sorted(decoded_char_count):
    print(f"'{char}': {decoded_char_count[char]} разів")

sorted_decoded_by_frequency = decoded_char_count.most_common()
print("\nЧастота повторення символів (по спаданню частоти):")
for char, count in sorted_decoded_by_frequency:
    print(f"'{char}': {count} разів")

# Гістограми частоти символів
plot_histogram(sorted(decoded_char_count.items()), "Гістограма розшифрованого тексту (в алфавітному порядку)", "Символ", "Частота")
plot_histogram(sorted_decoded_by_frequency, "Гістограма розшифрованого тексту (по спаданню частоти)", "Символ", "Частота")

# Підрахунок біграмів, тріграмів та чотириграмів для розшифрованого тексту
decoded_bigrams = find_ngrams(decoded_text, 2)
filtered_decoded_bigrams = decoded_bigrams.most_common(15)

decoded_trigrams = find_ngrams(decoded_text, 3)
filtered_decoded_trigrams = decoded_trigrams.most_common(15)

decoded_fourgrams = find_ngrams(decoded_text, 4)
filtered_decoded_fourgrams = decoded_fourgrams.most_common(15)

# Гістограми n-грамів для розшифрованого тексту
plot_histogram(filtered_decoded_bigrams, "Гістограма біграм розшифрованого тексту (15 найпоширеніших)", "Біграм", "Частота")
plot_histogram(filtered_decoded_trigrams, "Гістограма триграм розшифрованого тексту (15 найпоширеніших)", "Трьограм", "Частота")
plot_histogram(filtered_decoded_fourgrams, "Гістограма чотириграм розшифрованого тексту (15 найпоширеніших)", "Чотириграм", "Частота")

# Виведення повторень n-грамів для розшифрованого тексту
print("\nПовторення біграм розшифрованого тексту (15 найпоширеніших):")
for bigram, count in filtered_decoded_bigrams:
    print(f"'{bigram}': {count} разів")

print("\nПовторення триграм розшифрованого тексту (15 найпоширеніших):")
for trigram, count in filtered_decoded_trigrams:
    print(f"'{trigram}': {count} разів")

print("\nПовторення чотириграм розшифрованого тексту (15 найпоширеніших):")
for fourgram, count in filtered_decoded_fourgrams:
    print(f"'{fourgram}': {count} разів")
