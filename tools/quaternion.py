import serial
import time
import keyboard
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



v = [0, 0, 1]
square_size = 0.7

vx = [square_size, 0, 0]
vy = [0, square_size, 0]

theta = 0

def tune_yaw():
    global theta, v, vx, vy
    if keyboard.is_pressed('z'):
        theta += 1
        Z_rot = [np.cos(np.deg2rad(theta/2)), 0, 0, np.sin(np.deg2rad(theta/2))]
        v = rotate(v, Z_rot)
        vx = rotate(vx, Z_rot)
        vy = rotate(vy, Z_rot)
    elif keyboard.is_pressed('x'):
        theta -= 1
        Z_rot = [np.cos(np.deg2rad(theta/2)), 0, 0, np.sin(np.deg2rad(theta/2))]
        v = rotate(v, Z_rot)
        vx = rotate(vx, Z_rot)
        vy = rotate(vy, Z_rot)



def quaternion_to_euler(w, x, y, z):
    """ Преобразование кватерниона в углы Эйлера (последовательность ZYX) """
    roll = np.arctan2(2*(w*x + y*z), 1 - 2*(x*x + y*y))
    pitch = np.arcsin(2*(w*y - z*x))
    yaw = np.arctan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)

# Функции для работы с кватернионами
def quaternion_multiply(q1, q2):
    """Умножение двух кватернионов"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def rotate(v, q):
    """Поворот вектора кватернионом"""
    # Нормализация кватерниона
    q_norm = q / np.linalg.norm(q)
    # сопряженный кватернион
    q_conj = np.array([q_norm[0], -q_norm[1], -q_norm[2], -q_norm[3]])
    # кватернизируем вектор
    v_quat = np.array([0, *v])
    # Вычисление: q * v * q⁻¹
    rotated = quaternion_multiply(
        quaternion_multiply(q_norm, v_quat),
        q_conj
    )
    return rotated[1:]


def create_perpendicular_square(center, u, v):
    """Создание квадрата в плоскости, заданной векторами u и v"""
    return np.array([
        center + u + v,
        center + u - v,
        center - u - v,
        center - u + v,
        center + u + v  # замкнуть квадрат
    ])


# Настройка интерактивного графика
plt.ion()
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('MPU6050 orientation')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# начало координат
center = ax.scatter([0], [0], [0], c='k', s=100, marker='.')
# Начальный вектор
vector_line, = ax.plot([0, 0], [0, 0], [0, 1], 'r-', linewidth=2)
# Вектор гравитации
gravity_line, = ax.plot([0, 0], [0, 0], [0, 0], 'g-', linewidth=2)
# Квадрат, нормальный вектору
square_line, = ax.plot([], [], [], 'b-', linewidth=2, alpha=0.7)
# Добавление координатных осей
ax.quiver(0, 0, 0, 1.4, 0, 0, color='g', linestyle='-', linewidth=0.7)
ax.quiver(0, 0, 0, 0, 1.4, 0, color='g', linestyle='-', linewidth=0.7)
ax.quiver(0, 0, 0, 0, 0, 1.4, color='g', linestyle='-', linewidth=0.7)



# Проверка и открытие порта
try:
    ser = serial.Serial(f'COM5', 115200, timeout=1)
    print(f'COM5 открыт')
except serial.SerialException:
    print("Ошибка открытия COM-порта")
    exit()



# Основной цикл
try:
    while not keyboard.is_pressed('esc'):
        # Чтение телеметрии из порта
        telemetry = ser.readline().decode('utf-8').strip()
        
        if telemetry:
            try:
                # Парсинг serial
                data = [float(x) for x in telemetry.split(',')]
                
                if len(data) == 8:  # Кватернион + ускорения
                    quaternion = np.array(data[1:5])
                    accelerations = np.array(data[5:8])  # Линейные ускорения
                    
                    # Преобразование LSB в g (для ±16g: 2048 LSB/g)
                    accel_g = accelerations / 32768 * 16

                    # Поворот вектора
                    v_rot = rotate(v, quaternion)
                    a_rot = rotate(accel_g, quaternion)
                    r, p, y = quaternion_to_euler(quaternion[0], quaternion[1], quaternion[2], quaternion[3])

                    # вывод
                    print(f'Roll: {r:.2f}\tPitch: {p:.2f}\tYaw: {y:.2f}\taX: {a_rot[0]:.2f}\taY: {a_rot[1]:.2f}\ta: {np.linalg.norm(a_rot):.2f}')
                    
                    # Обновление графика
                    # Вектор
                    vector_line.set_data_3d(
                        [0, v_rot[0]],
                        [0, v_rot[1]],
                        [0, v_rot[2]]
                    )
                    # вектор ускорений
                    gravity_line.set_data_3d(
                        [0, a_rot[0]],
                        [0, a_rot[1]],
                        [0, a_rot[2]]
                    )
                    # Квадрат
                    square_points = create_perpendicular_square(
                        [0, 0, 0], 
                        rotate(vx, quaternion), 
                        rotate(vy, quaternion)
                    )
                    square_line.set_data_3d(
                        square_points[:, 0],
                        square_points[:, 1],
                        square_points[:, 2]
                    )
                    
                    # Перерисовка
                    tune_yaw()
                    fig.canvas.draw_idle()
                    plt.pause(0.01)
            
            except (ValueError, IndexError):
                print(f"Ошибка обработки данных: {telemetry}")
        
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    # Завершение работы
    ser.close()
    plt.ioff()
    plt.close()