import json
import os
import keyboard
import time


def init_json_config() -> dict:
    """ Создает новый config.json из default_config.json если конфига нет,
    или юзает существующий config.json """
    if not os.path.exists(os.path.join(os.getcwd(), 'config.json')):
        with open("default_config.json", "r", encoding="utf-8") as f:
            default_config = json.load(f)

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)

        return default_config
    else:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        return config


def read_joy_by_id(joystick, axes: list) -> list: 
    """ Принимает id осей джойстика и отдает список значений этих осей """
    return [joystick.get_axis(axis) for axis in axes]


def update_trims(config: dict, joystick) -> bool:
    """ Обновляет параметры триммеров в конфиге """
    is_config_updated = False
    for button, (param, delta) in config['binds']['joystick']['trim_buttons_id'].items():
        if joystick.get_button(int(button)):
            config['trims'][param] += delta
            is_config_updated = True

    return is_config_updated


def update_curves(config: dict) -> bool:
    """ Обновляет параметры кривых в конфиге """
    is_config_updated = False
    for button, (param, delta) in config['binds']['keyboard']['curves'].items():
        if keyboard.is_pressed(button):
            config['curves'][param] += delta
            is_config_updated = True
    
    return is_config_updated


def print_command_and_tele(c: str, t: dict) -> None:
    if t['status'] == 'Ok':
        tele_str = f"R: {t['roll']:.2f}\tP: {t['pitch']:.2f}\tY: {t['yaw']:.2f}\tn: {t['n']:.2f}\t\tV: {t['volts']:.2f}" 
    else:
        tele_str = t['status']

    print(f"\u2191 {c}\t\u2193 {tele_str}")


def upd_config(config: dict, joystick) -> None:
    """ Обновляет конфиг если нажимали конпки и если прошло время SAVE_INTERVAL """
    SAVE_INTERVAL = 5  # секунд между сохранениями

    # обновление триммеров и кривых
    need_update = update_trims(config, joystick) or update_curves(config)
    
    # Инициализация при первом вызове
    if not hasattr(upd_config, "last_save_time"):
        upd_config.last_save_time = time.time()
    
    # обновление
    if need_update and ((time.time() - upd_config.last_save_time) >= SAVE_INTERVAL):
        with open("config.json", "w") as f:
            json.dump(config, f, indent = 4)
        
        upd_config.last_save_time = time.time()
