def apply_curve(input: float, axis: str, config: dict) -> float:
    """ Применяет кривую вида x^a к осевой команде """
    output = abs(input) ** config['curves'][axis]
    if input < 0:
        return -output
    else:
        return output


def clamp(value, config: dict):
    """ Функция для ограничения значения в диапазоне 0-180 """
    return max(config['axes_norm']['min'], min(config['axes_norm']['max'], value))


def normalize_axis(value: float, axis: str, config: dict) -> int:
    """ Нормализация осевых команд """
    curved = apply_curve(value, axis, config) + 1
    normalized = curved * config['axes_norm']['max'] / 2
    trimmed = normalized + config['trims'][axis]
    clamped = clamp(trimmed, config)

    return int(clamped), int(normalized)