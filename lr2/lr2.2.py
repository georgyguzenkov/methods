import re
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# шифр сдвигом
def shift_cipher(text, shift, alphabet):
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            new_index = (alphabet.index(char) + shift) % len(alphabet)
            encrypted_text += alphabet[new_index]
        else:
            encrypted_text += char
    return encrypted_text

# шифр виженером
def vigenere_cipher(text, key, alphabet):
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted_text = ""
    for char, key_char in zip(text, key):
        if char in alphabet:
            shift = alphabet.index(key_char)
            new_index = (alphabet.index(char) + shift) % len(alphabet)
            encrypted_text += alphabet[new_index]
        else:
            encrypted_text += char
    return encrypted_text

# шифр lfsr
def lfsr_cipher(text, seed, polynomial, alphabet):
    state = seed[:]
    encrypted_text = ""
    for char in text:
        if char in alphabet:
            bit = state[0]
            new_index = (alphabet.index(char) + bit) % len(alphabet)
            encrypted_text += alphabet[new_index]
            feedback = sum(state[i] for i in polynomial) % 2
            state = state[1:] + [feedback]
        else:
            encrypted_text += char
    return encrypted_text

# функция для построения гистограммы
def plot_histogram(text, alphabet):
    frequencies = {char: text.count(char) for char in alphabet}
    plt.bar(frequencies.keys(), frequencies.values())
    plt.xlabel("Символы")
    plt.ylabel("Частота")
    plt.title("Гистограмма частотности символов")
    plt.show()

def create_gui():
    root = tk.Tk()
    root.title("Шифрование текста")
    root.geometry("600x400")

    # Переменные для хранения выбранных значений
    selected_method = tk.StringVar(value="1")
    constant_value = tk.StringVar()
    file_path = [""]  # Используем список для хранения пути к файлу

    def browse_file():
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            file_path[0] = path
            file_label.config(text=f"Выбран файл: {path.split('/')[-1]}")

    def process_file():
        if not file_path[0]:
            messagebox.showerror("Ошибка", "Выберите файл!")
            return

        try:
            with open(file_path[0], 'r', encoding='utf-8') as file:
                text = re.sub(r'[^А-Я]', '', file.read().upper().replace("Ё", "Е"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")
            return

        method = selected_method.get()
        alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ"

        try:
            if method == "1":
                if not constant_value.get():
                    messagebox.showerror("Ошибка", "Введите константу!")
                    return
                shift = int(constant_value.get()) % len(alphabet)
                encrypted_text = shift_cipher(text, shift, alphabet)
            elif method == "2":
                if not constant_value.get():
                    messagebox.showerror("Ошибка", "Введите ключевое слово!")
                    return
                key = constant_value.get().upper().replace("Ё", "Е")
                key = re.sub(r'[^А-Я]', '', key)
                encrypted_text = vigenere_cipher(text, key, alphabet)
            elif method == "3":
                seed = [random.randint(0, 1) for _ in range(5)]
                polynomial = [0, 2]
                encrypted_text = lfsr_cipher(text, seed, polynomial, alphabet)
                plot_histogram(encrypted_text, alphabet)

            output_file = file_path[0].replace(".txt", "_encrypted.txt")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(encrypted_text)
            
            messagebox.showinfo("Успех", 
                f"Текст успешно зашифрован!\nРезультат сохранен в:\n{output_file}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def update_constant_label(*args):
        method = selected_method.get()
        if method == "1":
            constant_label.config(text="Введите константу (номер студента):")
        elif method == "2":
            constant_label.config(text="Введите ключевое слово (поговорку):")
        else:
            constant_label.config(text="Константа не требуется")

    # Создаем и размещаем элементы интерфейса
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Метод шифрования
    method_label = ttk.Label(frame, text="Выберите метод шифрования:")
    method_label.grid(row=0, column=0, pady=10, sticky=tk.W)

    methods_frame = ttk.Frame(frame)
    methods_frame.grid(row=1, column=0, pady=5, sticky=tk.W)

    ttk.Radiobutton(methods_frame, text="Шифр сдвигом", variable=selected_method, 
                    value="1", command=update_constant_label).grid(row=0, column=0, sticky=tk.W)
    ttk.Radiobutton(methods_frame, text="Шифр Виженера", variable=selected_method, 
                    value="2", command=update_constant_label).grid(row=1, column=0, sticky=tk.W)
    ttk.Radiobutton(methods_frame, text="LFSR", variable=selected_method, 
                    value="3", command=update_constant_label).grid(row=2, column=0, sticky=tk.W)

    # Поле для ввода константы
    constant_label = ttk.Label(frame, text="Введите константу (номер студента):")
    constant_label.grid(row=2, column=0, pady=10, sticky=tk.W)
    
    constant_entry = ttk.Entry(frame, width=40, textvariable=constant_value)
    constant_entry.grid(row=3, column=0, pady=5, sticky=tk.W)

    # Кнопка выбора файла
    browse_button = ttk.Button(frame, text="Обзор...", command=browse_file)
    browse_button.grid(row=4, column=0, pady=10, sticky=tk.W)

    # Метка для отображения выбранного файла
    file_label = ttk.Label(frame, text="Файл не выбран")
    file_label.grid(row=5, column=0, pady=5, sticky=tk.W)

    # Кнопка выполнения
    execute_button = ttk.Button(frame, text="Выполнить", command=process_file)
    execute_button.grid(row=6, column=0, pady=20)

    # Инициализация метки константы
    update_constant_label()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
