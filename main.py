import matplotlib
import numpy as np

matplotlib.use('TkAgg')  # Встановлюємо бекенд для Matplotlib перед імпортом pyplot
import matplotlib.pyplot as plt
from collections import Counter  # Додаємо Counter у main.py

import feistel_cipher
import hill_cipher
import vigener_cipher
import rsa_cipher


def main():
    while True:
        print("\n\n")
        print("Виберіть шифр для запуску:")
        print("1 - Hill Cipher")
        print("2 - Feistel Cipher")
        print("3 - Vigener Cipher")
        print("4 - RSA Cipher")
        print("0 - Вийти з програми")

        choice = input("Введіть номер (0-4): ").strip()

        if choice == '1':
            print("Запускаємо Hill Cipher...")
            hill_cipher.main()
        elif choice == '2':
            print("Запускаємо Feistel Cipher...")
            feistel_cipher.main()
        elif choice == '3':
            print("Запускаємо Vigener Cipher...")
            vigener_cipher.main()
        elif choice == '4':
            print("Запускаємо RSA Cipher...")
            rsa_cipher.main()
        elif choice == '0':
            print("Вихід з програми...")
            break  # Завершуємо цикл і виходимо з програми
        else:
            print("Помилка: Введіть цифру від 0 до 4.")

        # Додаємо паузу, щоб користувач міг прочитати результат перед поверненням до меню
        input("Натисніть Enter, щоб повернутися до меню...")


if __name__ == "__main__":
    main()