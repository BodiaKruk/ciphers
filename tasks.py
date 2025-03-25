from invoke import task

import unittest
import os
import shutil

@task
def clean(c):
    # Видаляє тимчасові файли PyInstaller
    print("Очищення старих файлів...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("__pycache__", ignore_errors=True)
    if os.path.exists("main.spec"):
        os.remove("main.spec")
    print("Очищення завершено!")

@task
def test(c):
    # Запускає модульні тести перед збіркою
    print("Запуск модульних тестів...")
    result = c.run("python -m unittest test_rsa_cipher.py", warn=True)
    if result.failed:
        print("Помилка в тестах! Збірку скасовано.")
        exit(1)
    print("Тести пройдено успішно!")

@task
def build(c):
    # Збирає виконуваний файл з main.py
    print("Запуск PyInstaller...")
    c.run("pyinstaller --onefile --icon=bill-cipher.ico --name=main main.py")
    print("Збірка завершена!")

@task
def run(c):
    # Запускає виконуваний файл після збірки
    exe_path = os.path.join("dist", "main.exe" if os.name == "nt" else "main")
    if os.path.exists(exe_path):
        print(f"Запуск {exe_path}...")
        c.run(exe_path)
    else:
        print("Виконуваний файл не знайдено. Спочатку виконай `invoke build`.")

@task
def full_build(c):
    # Очищення старих файлів + тестування + нова збірка
    clean(c)
    test(c)
    build(c)
