import random
import sympy
import tkinter as tk
from tkinter import messagebox, ttk

#шифр диффи-хеллман
def diffie_hellman(p, g, private_a, private_b):
    public_a = pow(g, private_a, p)
    public_b = pow(g, private_b, p)
    shared_key_a = pow(public_b, private_a, p)
    shared_key_b = pow(public_a, private_b, p)
    assert shared_key_a == shared_key_b
    return shared_key_a

#генерация rsa
def generate_rsa_keys():
    p = sympy.randprime(100, 500)
    q = sympy.randprime(100, 500)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    return (e, n), (d, n)

#шифр rsa
def rsa_encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

#дешифр rsa
def rsa_decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ''.join(chr(pow(char, d, n)) for char in encrypted_message)
    return decrypted_message

def create_gui():
    root = tk.Tk()
    root.title("Криптографические методы")
    root.geometry("600x500")

    # Переменные для хранения выбранных значений
    selected_method = tk.StringVar(value="1")
    p_value = tk.StringVar()
    g_value = tk.StringVar()
    private_a_value = tk.StringVar()
    private_b_value = tk.StringVar()
    message_value = tk.StringVar()

    def process_encryption():
        method = selected_method.get()
        
        try:
            if method == "1":
                # Проверка ввода для Диффи-Хеллмана
                if not all([p_value.get(), g_value.get(), private_a_value.get(), private_b_value.get()]):
                    messagebox.showerror("Ошибка", "Заполните все поля!")
                    return
                
                p = int(p_value.get())
                g = int(g_value.get())
                private_a = int(private_a_value.get())
                private_b = int(private_b_value.get())
                
                shared_key = diffie_hellman(p, g, private_a, private_b)
                messagebox.showinfo("Результат", f"Общий ключ: {shared_key}")
            
            elif method == "2":
                # Генерация и использование RSA
                public_key, private_key = generate_rsa_keys()
                
                if not message_value.get():
                    messagebox.showerror("Ошибка", "Введите сообщение!")
                    return
                
                message = message_value.get()
                encrypted = rsa_encrypt(message, public_key)
                decrypted = rsa_decrypt(encrypted, private_key)
                
                result_text = f"Открытый ключ: {public_key}\n"
                result_text += f"Закрытый ключ: {private_key}\n"
                result_text += f"Зашифрованное сообщение: {encrypted}\n"
                result_text += f"Расшифрованное сообщение: {decrypted}"
                
                messagebox.showinfo("Результат", result_text)
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def update_fields(*args):
        method = selected_method.get()
        if method == "1":
            # Показываем поля для Диффи-Хеллмана
            p_frame.grid()
            g_frame.grid()
            private_a_frame.grid()
            private_b_frame.grid()
            message_frame.grid_remove()
        else:
            # Показываем поле для RSA
            p_frame.grid_remove()
            g_frame.grid_remove()
            private_a_frame.grid_remove()
            private_b_frame.grid_remove()
            message_frame.grid()

    # Создаем и размещаем элементы интерфейса
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Метод шифрования
    method_label = ttk.Label(frame, text="Выберите метод:")
    method_label.grid(row=0, column=0, pady=10, sticky=tk.W)

    methods_frame = ttk.Frame(frame)
    methods_frame.grid(row=1, column=0, pady=5, sticky=tk.W)

    ttk.Radiobutton(methods_frame, text="Диффи-Хеллман", variable=selected_method, 
                    value="1", command=update_fields).grid(row=0, column=0, sticky=tk.W)
    ttk.Radiobutton(methods_frame, text="RSA", variable=selected_method, 
                    value="2", command=update_fields).grid(row=1, column=0, sticky=tk.W)

    # Поля для Диффи-Хеллмана
    p_frame = ttk.Frame(frame)
    p_frame.grid(row=2, column=0, pady=5, sticky=tk.W)
    ttk.Label(p_frame, text="Простое число p:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(p_frame, textvariable=p_value, width=40).grid(row=0, column=1, padx=5)

    g_frame = ttk.Frame(frame)
    g_frame.grid(row=3, column=0, pady=5, sticky=tk.W)
    ttk.Label(g_frame, text="Первообразный корень g:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(g_frame, textvariable=g_value, width=40).grid(row=0, column=1, padx=5)

    private_a_frame = ttk.Frame(frame)
    private_a_frame.grid(row=4, column=0, pady=5, sticky=tk.W)
    ttk.Label(private_a_frame, text="Приватный ключ A:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(private_a_frame, textvariable=private_a_value, width=40).grid(row=0, column=1, padx=5)

    private_b_frame = ttk.Frame(frame)
    private_b_frame.grid(row=5, column=0, pady=5, sticky=tk.W)
    ttk.Label(private_b_frame, text="Приватный ключ B:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(private_b_frame, textvariable=private_b_value, width=40).grid(row=0, column=1, padx=5)

    # Поле для RSA
    message_frame = ttk.Frame(frame)
    message_frame.grid(row=2, column=0, pady=5, sticky=tk.W)
    ttk.Label(message_frame, text="Введите фамилию и инициалы:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(message_frame, textvariable=message_value, width=40).grid(row=0, column=1, padx=5)

    # Кнопка выполнения
    execute_button = ttk.Button(frame, text="Выполнить", command=process_encryption)
    execute_button.grid(row=6, column=0, pady=20)

    # Инициализация полей
    update_fields()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
