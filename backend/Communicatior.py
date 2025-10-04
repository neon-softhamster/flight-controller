import pygame
import serial
import time
import backend.func.command_utils as com_u
import backend.func.controller_utils as ctrl_u
import backend.func.telemetry_utils as tele_u



class Communicator:
    def __init__(self, data_queue):
        pygame.init()
        pygame.joystick.init()

        self.error_list = []
        self.queue = data_queue

        # Проверка подключенных джойстиков
        if pygame.joystick.get_count() == 0:
            problem = "No joystick. Plug in and restart."
            print(problem)
            self.error_list.append(problem)
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick: \"{self.joystick.get_name()}\".")

        # Инициализация конфига
        self.config = ctrl_u.init_json_config()

        # Проверка и открытие порта
        try:
            self.ser = serial.Serial(
                f'COM{self.config['serial']['port']}', 
                self.config['serial']['rate'], 
                timeout = self.config['serial']['timeout']
            )
            print(f'COM{self.config['serial']['port']} is opened.')
        except serial.SerialException:
            problem = "COM port error. Check if transmitter is connected to the port specified in config."
            print(problem)
            self.error_list.append(problem)
    

    def self_check(self):
        if len(self.error_list) == 0:
            return True
        else: 
            return False


    def run(self, stop):
        while not stop.is_set():
            try:
                pygame.event.pump()

                # Чтение осей
                axis_x, axis_y, axis_z, slider = ctrl_u.read_joy_by_id(self.joystick, [0, 1, 2, 5])

                # нормализация осей
                x, x_norm = com_u.normalize_axis(axis_x, 'x', self.config)
                y, y_norm = com_u.normalize_axis(axis_y, 'y', self.config)
                z, z_norm = com_u.normalize_axis(axis_z, 'z', self.config)
                t = int((((-slider +  1) / 2) ** self.config['curves']['t']) * 255)

                # отправка команды в порт
                command = f"{x},{y},{z},{t}."
                command_for_interface = (
                    [x_norm, y_norm, z_norm], # no trim
                    [x, y, z, t] # trim
                )
                self.ser.write(command.encode('utf-8'))

                # чтение телеметрии из порта
                telemetry = tele_u.get_telemetry(self.ser, self.config)

                # печать команды и телеметрии
                ctrl_u.print_command_and_tele(command, telemetry)

                # Помещаем данные в очередь
                self.queue.put((
                    command_for_interface, 
                    telemetry, 
                    self.config
                ))
                
                # сохранение config
                ctrl_u.upd_config(self.config, self.joystick)

                # задержка
                time.sleep(self.config['command_interval'])
            except Exception as e:
                print(f'Backend thread in Communicator.run(): "{e}"')

        pygame.quit()

        # закрываем порт при выходе, если открыт
        if self.ser and self.ser.is_open:
            self.ser.close()