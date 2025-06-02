import tkinter as tk
from tkinter import messagebox, ttk
import sympy

# Функция для поиска простых делителей числа n
def prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return list(factors)

# Функция для поиска примитивного корня по модулю p
def find_primitive_root(p):
    if not sympy.isprime(p):
        return None
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return None

def create_gui():
    root = tk.Tk()
    root.title("Поиск примитивного корня")
    root.geometry("400x200")

    p_value = tk.StringVar()

    def process():
        try:
            p = int(p_value.get())
            if p < 2:
                messagebox.showerror("Ошибка", "Введите простое число больше 1!")
                return
            g = find_primitive_root(p)
            if g is not None:
                messagebox.showinfo("Результат", f"Примитивный корень по модулю {p}: {g}")
            else:
                messagebox.showerror("Ошибка", "Число не является простым или примитивный корень не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")

    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    label = ttk.Label(frame, text="Введите простое число p:")
    label.grid(row=0, column=0, pady=10, sticky=tk.W)

    entry = ttk.Entry(frame, width=30, textvariable=p_value)
    entry.grid(row=1, column=0, pady=5, sticky=tk.W)

    button = ttk.Button(frame, text="Выполнить", command=process)
    button.grid(row=2, column=0, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui() 