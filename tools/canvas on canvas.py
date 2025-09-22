import tkinter as tk

root = tk.Tk()

# Создаем родительский Canvas
parent_canvas = tk.Canvas(root, width=400, height=400, bg="white")
parent_canvas.pack()

# Создаем дочерний Canvas с заданными размерами
child_canvas = tk.Canvas(parent_canvas, width=200, height=200, bg="lightblue")

# Размещаем дочерний Canvas на родительском в точке (100, 150)
parent_canvas.create_window(100, 150, window=child_canvas)

# Добавляем элементы на дочерний Canvas для демонстрации
child_canvas.create_rectangle(10, 10, 190, 90, fill="red")
child_canvas.create_text(100, 150, text="Дочерний Canvas")

root.mainloop()