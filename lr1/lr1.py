import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
import math
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Вывод таблицы встречаемости символов
def print_frequency_table(freq):
    print("\nСимвол | Частота")
    print("----------------")
    for char, count in sorted(freq.items()):
        print(f"  {char:3}  | {count}")

# Анализ текста
def analyze_text(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    freq = Counter(data)
    return freq

# Анализ фото
def analyze_bmp(file_path):
    img = Image.open(file_path)
    img = img.convert("RGB")
    pixels = np.array(img)
    channels = ['Red', 'Green', 'Blue']
    freq = {ch: Counter() for ch in channels}
    
    for i, ch in enumerate(channels):
        freq[ch] = Counter(pixels[:, :, i].flatten())
    
    return freq

# Подсчет энтропии
def calculate_entropy(freq, total):
    entropy = -sum((count / total) * math.log2(count / total) for count in freq.values())
    return entropy

# Построение гистограммы
def plot_histogram(freq, title):
    plt.figure(figsize=(10, 5))
    plt.bar(freq.keys(), freq.values(), color='blue')
    plt.xlabel("Значения (0-255)")
    plt.ylabel("Частота")
    plt.title(title)
    plt.show()

def create_gui():
    root = tk.Tk()
    root.title("Анализ файлов")
    root.geometry("400x200")

    def select_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("BMP files", "*.bmp")]
        )
        if file_path:
            try:
                if file_path.endswith(".txt"):
                    freq = analyze_text(file_path)
                    total_chars = sum(freq.values())
                    entropy = calculate_entropy(freq, total_chars)
                    result_text = f"Энтропия текста: {entropy:.4f} бит/символ\n"
                    result_text += "\nСимвол | Частота\n----------------\n"
                    for char, count in sorted(freq.items()):
                        result_text += f"  {char:3}  | {count}\n"
                    messagebox.showinfo("Результаты анализа", result_text)
                    plot_histogram(freq, "Частотный анализ текста")
                elif file_path.endswith(".bmp"):
                    freq = analyze_bmp(file_path)
                    result_text = ""
                    for ch, data in freq.items():
                        total_pixels = sum(data.values())
                        entropy = calculate_entropy(data, total_pixels)
                        result_text += f"Энтропия {ch} канала: {entropy:.4f} бит/символ\n"
                        result_text += "\nСимвол | Частота\n----------------\n"
                        for char, count in sorted(data.items()):
                            result_text += f"  {char:3}  | {count}\n"
                        result_text += "\n"
                    messagebox.showinfo("Результаты анализа", result_text)
                    for ch, data in freq.items():
                        plot_histogram(data, f"Частотный анализ {ch} канала")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при анализе файла: {str(e)}")

    # Создаем и размещаем элементы интерфейса
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    label = ttk.Label(frame, text="Выберите файл для анализа (TXT или BMP):")
    label.grid(row=0, column=0, pady=20)

    browse_button = ttk.Button(frame, text="Обзор...", command=select_file)
    browse_button.grid(row=1, column=0, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
