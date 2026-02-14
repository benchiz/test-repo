import tkinter as tk
from tkinter import messagebox

def add_numbers():
    try:
        # Получаем текст из полей ввода и преобразуем в числа
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        
        # Считаем сумму
        result = num1 + num2
        
        # Выводим результат в текстовое поле
        result_label.config(text=f"Результат: {result}")
    except ValueError:
        # Если введено не число — показываем ошибку
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа!")

# Создаём главное окно
window = tk.Tk()
window.title("Простой калькулятор")
window.geometry("300x200")
window.resizable(False, False)  # Запрещаем изменение размера окна

# Надпись над первым полем ввода
tk.Label(window, text="Первое число:").pack(pady=5)

# Поле ввода для первого числа
entry1 = tk.Entry(window, width=20)
entry1.pack(pady=5)

# Надпись над вторым полем ввода
tk.Label(window, text="Второе число:").pack(pady=5)

# Поле ввода для второго числа
entry2 = tk.Entry(window, width=20)
entry2.pack(pady=5)

# Кнопка для вычисления суммы
add_button = tk.Button(window, text="Сложить", command=add_numbers)
add_button.pack(pady=10)

# Область для вывода результата
result_label = tk.Label(window, text="Результат: ", font=("Arial", 10))
result_label.pack(pady=10)

# Запускаем главный цикл обработки событий
window.mainloop()
