import tkinter as tk
from math import sin, cos, radians

# Создаем основное окно
root = tk.Tk()
root.title("Авиагоризонт")

# Размеры элементов
canvas_width = 400
canvas_height = 400
square_size = 300
hole_radius = 100
rectangle_height = 200  # Высота нижнего прямоугольника (земли)

# Создаем холст
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Расчет координат
square_x0 = (canvas_width - square_size) // 2
square_y0 = (canvas_height - square_size) // 2
square_x1 = square_x0 + square_size
square_y1 = square_y0 + square_size

hole_center_x = canvas_width // 2
hole_center_y = canvas_height // 2

# Рисуем нижний прямоугольник (землю)
canvas.create_rectangle(
    0, hole_center_y,  # Верхний левый угол
    canvas_width, canvas_height,  # Нижний правый угол
    fill='#8B4513',  # Коричневый цвет земли
    outline=''
)

# Рисуем верхний прямоугольник (небо)
canvas.create_rectangle(
    0, 0,  # Верхний левый угол
    canvas_width, hole_center_y,  # Нижний правый угол
    fill='#87CEEB',  # Голубой цвет неба
    outline=''
)

# Создаем черный квадрат с отверстием через создание многоугольника
points = []
# Внешний контур квадрата
points.extend([square_x0, square_y0])
points.extend([square_x1, square_y0])
points.extend([square_x1, square_y1])
points.extend([square_x0, square_y1])
points.extend([square_x0, square_y0])

# Добавляем начальную точку отверстия
points.extend([hole_center_x + hole_radius, hole_center_y])

# Генерируем точки для круга (в обратном порядке для обхода против часовой стрелки)
for angle in range(360, 0, -10):
    x = hole_center_x + hole_radius * cos(radians(angle))
    y = hole_center_y - hole_radius * sin(radians(angle))
    points.extend([x, y])

# Замыкаем отверстие
points.extend([hole_center_x + hole_radius, hole_center_y])

# Рисуем фигуру
canvas.create_polygon(
    points,
    fill='black',
    outline='black',
    smooth=True  # Сглаживаем края отверстия
)

root.mainloop()