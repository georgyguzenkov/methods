import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# создание таблицы по ключу
def generate_playfair_table(key):
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ"
    key = "".join(dict.fromkeys(key.upper().replace("Ё", "Е")))
    table = key + "".join(c for c in alphabet if c not in key)
    return [list(table[i:i+5]) for i in range(0, 25, 5)]

# поиск позиции
def find_position(table, letter):
    for row in range(5):
        for col in range(5):
            if table[row][col] == letter:
                return row, col
    return None

# дешифрование по варианту 6
def playfair_decrypt(text, table):
    text = re.sub(r'[^А-ЯЁ]', '', text.upper().replace("Ё", "Е"))
    text_pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) and text[i] != text[i+1] else 'Х'
        if find_position(table, a) is None or find_position(table, b) is None:
            i += 1
            continue
        text_pairs.append((a, b))
        i += 2 if text[i] != b else 1

    decrypted_text = ""
    for a, b in text_pairs:
        row1, col1 = find_position(table, a)
        row2, col2 = find_position(table, b)
        if row1 is None or row2 is None:
            continue
        if row1 == row2:
            decrypted_text += table[row1][(col1-1)%5] + table[row2][(col2-1)%5]
        elif col1 == col2:
            decrypted_text += table[(row1-1)%5][col1] + table[(row2-1)%5][col2]
        else:
            decrypted_text += table[row1][col2] + table[row2][col1]
    return decrypted_text

def create_gui():
    root = tk.Tk()
    root.title("Дешифрование шифра Плейфера")
    root.geometry("500x300")

    def process_file():
        key = key_entry.get().strip()
        if not key:
            messagebox.showerror("Ошибка", "Введите ключ!")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                table = generate_playfair_table(key)
                decrypted_text = playfair_decrypt(text, table)
                output_file = file_path.replace(".txt", "_decrypted.txt")
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(decrypted_text)
                messagebox.showinfo("Успех", 
                    f"Текст успешно дешифрован!\nРезультат сохранен в:\n{output_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    # Создаем и размещаем элементы интерфейса
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Поле для ввода ключа
    key_label = ttk.Label(frame, text="Введите ключ:")
    key_label.grid(row=0, column=0, pady=10, sticky=tk.W)
    
    key_entry = ttk.Entry(frame, width=40)
    key_entry.grid(row=1, column=0, pady=5, sticky=tk.W)

    # Кнопка выбора файла
    browse_button = ttk.Button(frame, text="Выбрать зашифрованный файл...", command=process_file)
    browse_button.grid(row=2, column=0, pady=20)

    # Инструкции
    instructions = ttk.Label(frame, text="Выберите зашифрованный текстовый файл для дешифрования.\nРезультат будет сохранен в новый файл с суффиксом '_decrypted'.")
    instructions.grid(row=3, column=0, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui() 