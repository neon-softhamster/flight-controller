from styles.Style import *



class InfoBar:
    def __init__(self, master):
        NUM_INDICATORS = 10  # Количество индикаторов
        INDICATOR_HEIGHT = 40  # Высота индикаторов
        TEXT_COLOR = 'white'  # Цвет текста
        COLORS = [  # Цвета для индикаторов
            '#FF5733', '#33FF57', '#3357FF', '#F333FF', '#FF33A1',
            '#FF5733', "#33ADFF", '#3357FF', '#F333FF', '#FF33A1'
        ]
        width = 1920 - 1.5
        
        # Рассчитываем ширину одного индикатора
        indicator_width = width / NUM_INDICATORS
        
        for i in range(NUM_INDICATORS):
            # Координаты прямоугольника
            x0 = i * indicator_width
            y0 = 641
            x1 = (i + 1) * indicator_width
            y1 = y0 + INDICATOR_HEIGHT
            
            # Рисуем прямоугольник
            master.create_rectangle(
                x0, y0, x1, y1,
                fill=COLORS[i % len(COLORS)],
                outline=''
            )
            
            # Добавляем текст
            text_x = (x0 + x1) / 2
            text_y = (y0 + y1) / 2
            master.create_text(
                text_x, text_y,
                text=f"Info {i+1}",
                fill=TEXT_COLOR,
                font=defaultTextStyle
            )