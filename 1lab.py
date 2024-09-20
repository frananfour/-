# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext
from collections import Counter
import pymorphy2
import re


# Функция для нормализации слова
def normalize_word(word, morph):
    parsed_word = morph.parse(word)[0]
    return parsed_word.normal_form


# Функция для подсчета слов
def count_words():
    # Получаем текст из текстового поля
    text = input_text.get("1.0", tk.END).lower()

    # Убираем лишние символы, кроме слов и пробелов
    words = re.findall(r'\b\w+\b', text)

    # Инициализируем pymorphy2
    morph = pymorphy2.MorphAnalyzer()

    # Нормализуем слова
    normalized_words = [normalize_word(word, morph) for word in words]

    # Подсчитываем количество каждого слова
    word_count = Counter(normalized_words)

    # Сортируем по убыванию частоты
    sorted_words = word_count.most_common()

    # Формируем вывод
    output = []
    for word, count in sorted_words:
        output.append(f"{word} — {count}")

    # Вставляем результат в текстовое поле для вывода
    result_text.delete("1.0", tk.END)  # Очистка предыдущего результата
    if output:
        result_text.insert(tk.END, "\n".join(output))
    else:
        result_text.insert(tk.END, "Нет слов для анализа")


# Создаем окно приложения
window = tk.Tk()
window.title("Подсчет слов")

# Поле для ввода текста
input_label = tk.Label(window, text="Введите текст:")
input_label.pack()

input_text = scrolledtext.ScrolledText(window, width=60, height=10)
input_text.pack()

# Кнопка для обработки текста
process_button = tk.Button(window, text="Подсчитать слова", command=count_words)
process_button.pack()

# Поле для вывода результата
result_label = tk.Label(window, text="Результаты:")
result_label.pack()

result_text = scrolledtext.ScrolledText(window, width=60, height=10)
result_text.pack()

# Запуск основного цикла приложения
window.mainloop()