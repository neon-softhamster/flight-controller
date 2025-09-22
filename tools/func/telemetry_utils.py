import numpy as np



# Функции для работы с кватернионами
def quaternion_multiply(q1, q2):
    """ Умножение двух кватернионов """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])


def rotate(v, q):
    """ Поворот вектора кватернионом """
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


def quaternion_to_euler(q):
    """ Преобразование кватерниона roll, pitch и yaw в градусах """
    w, x, y, z = q
    roll = np.arctan2(2*(w*x + y*z), 1 - 2*(x*x + y*y))
    pitch = np.arcsin(2*(w*y - z*x))
    yaw = np.arctan2(2*(w*z + x*y), 1 - 2*(y*y + z*z))
    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)


def parse_telemetry(telemetry: str) -> dict:
    """ Парсит телеметрию. Принимает проверенную строку """
    tele_data = [float(x) for x in telemetry.split(',')]

    quaternion = np.array(tele_data[1:5]) # кватернион поворота
    accelerations = np.array(tele_data[5:8]) # Линейные ускорения

    parsed = {}
    parsed['roll'], parsed['pitch'], parsed['yaw'] = quaternion_to_euler(quaternion)
    parsed['ax'], parsed['ay'], parsed['az'] = rotate(accelerations / 32768 * 16, quaternion)
    parsed['a_total'] = np.linalg.norm([parsed['ax'], parsed['ay'], parsed['az']])
    parsed['n'] = parsed['a_total'] / 9.81
    parsed['volts'] = tele_data[0]

    return parsed


def get_telemetry(ser, config: dict):
    telemetry = {}
    if ser.in_waiting > 0:
        tele_str = ser.readline().decode('utf-8').strip()

        if tele_str.count(',') == config['telemetry_length'] - 1:
            telemetry = parse_telemetry(tele_str)
            telemetry['status'] = 'Ok'
        else:
            telemetry['status'] = f"Telemetry error: telemetry = {tele_str}"
    else:
        telemetry['status'] = f"Telemetry error: no telemetry"
    
    return telemetry
    