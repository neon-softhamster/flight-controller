import pygame
import time
import keyboard

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Джойстик не найден!")
    exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()

joy_name = joystick.get_name()
print(f"Джойстик: {joy_name}")
if joy_name == 'WINWING URSA MINOR FIGHTER FLIGHT STICK L':
    btn_id_to_pass = [49]

n_axes = joystick.get_numaxes()
n_buttons = joystick.get_numbuttons()
mode = 'a'

last_key = None
def on_key_press(event):
    global last_key
    last_key = event.name
keyboard.on_press(on_key_press)

while not keyboard.is_pressed('esc'):
    pygame.event.pump()  # Обработка событий

    if last_key:
        # print(f"Зарегистрирована клавиша: {last_key}")
        last_key = None  # Сбрасываем значение

    if keyboard.is_pressed('left'):
        print('Режим просмотра осей')
        mode = 'a'
    elif keyboard.is_pressed('right'):
        print('Режим просмотра кнопок')
        mode = 'b'

    if mode == 'a':
        # Чтение осей
        axes_values = ''
        for ax in range(n_axes):
            axes_values += f'ID:{ax} -> {joystick.get_axis(ax):.2f},\t'
        print(axes_values)
    elif mode == 'b':
        # Чтение кнопок
        for button_id in range(n_buttons):
            if joystick.get_button(button_id) and button_id not in btn_id_to_pass:
                print(f"ID:{button_id}")

    time.sleep(0.1)
keyboard.unhook_all()