import pygame
import serial
import time
import keyboard
import func.command_utils as com_u
import func.controller_utils as ctrl_u
import func.telemetry_utils as tele_u



pygame.init()
pygame.joystick.init()

# Проверка подключенных джойстиков
if pygame.joystick.get_count() == 0:
    print("No joystick. Plug in and restart.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Joystick: \"{joystick.get_name()}\".")

# Инициализация конфига
config = ctrl_u.init_json_config()
is_config_dirty = False
last_save_time = 0

# Проверка и открытие порта
try:
    ser = serial.Serial(
        f'COM{config['serial']['port']}', 
        config['serial']['rate'], 
        timeout = config['serial']['timeout']
    )
    print(f'COM{config['serial']['port']} is opened.')
except serial.SerialException:
    print("COM port error. Check if transmitter is connected to the port specified.")
    exit()

# Основной цикл
try:
    while not keyboard.is_pressed('esc'):
        pygame.event.pump()  # Обработка событий

        # Чтение осей
        axis_x, axis_y, axis_z, slider = ctrl_u.read_joy_by_id(joystick, [0, 1, 2, 5])
        # print(f"X: {axis_x:.4f}, Y: {axis_y:.4f}, Z: {axis_z:.4f}, Slider: {slider:.4f}")

        # нормализация осей
        x_norm = com_u.normalize_axis(axis_x, 'x', config)
        y_norm = com_u.normalize_axis(axis_y, 'y', config)
        z_norm = com_u.normalize_axis(axis_z, 'z', config)
        t_norm = int((((-slider +  1) / 2) ** config['curves']['t']) * 255)

        # отправка команды в порт
        command = f"{x_norm},{y_norm},{z_norm},{t_norm}."
        ser.write(command.encode('utf-8'))

        # чтение телеметрии из порта
        telemetry = tele_u.get_telemetry(ser, config)

        # печать команды и телеметрии
        ctrl_u.print_command_and_tele(command, telemetry)
         
        # сохранение config
        ctrl_u.upd_config(config, joystick)

        # задержка
        time.sleep(config['command_interval'])

except KeyboardInterrupt:
    ser.close()
    pygame.quit()