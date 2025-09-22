from styles.Style import *
import tkinter as tk
import numpy as np



class NavBall:
    def __init__(self, master_canvas, size, **kwargs):
        ypr_ind_v_space = kwargs.get('YPR_Vspace', 30)
        ypr_ind_pos = kwargs.get('YPR_pos', (15, 15))
        horizon_bar_width = kwargs.get('horizon_bar_width', 70)
        horizon_px_per_grad = kwargs.get('horizon_px_per_grad', 7)
        level_color = kwargs.get('level_color', 'DarkOrange')
        level_size = kwargs.get('level_size', 140)
        roll_ruler_size = kwargs.get('roll_ruler_size', 170)
        roll_ruler_major_marks = kwargs.get('roll_ruler_major_marks', [-30, 0, 30, 90, 150, 180, 210])
        roll_ruler_minor_marks = kwargs.get('roll_ruler_minor_marks', [10, 20, 45, 135, 160, 170])

        self.width, self.height = size
        self.main = tk.Canvas(
            master_canvas, 
            width=self.width, 
            height=self.height, 
            bg="CornflowerBlue"
        )

        # создание элементов навбола
        self.ypr_indicators = YPR_indicator(
            self.main,
            ypr_ind_pos,
            ypr_ind_v_space,
        )
        self.horizon = Horizon(
            self.main, 
            horizon_bar_width, 
            horizon_px_per_grad
        )
        self.level = Level(
            self.main, 
            level_color, 
            level_size
        )
        self.roll_ruler = RollRuler(
            self.main, 
            roll_ruler_size, 
            roll_ruler_major_marks, 
            roll_ruler_minor_marks,
        )


    def update(self, ypr):
        """ Обновление навбола при поступлении новых данных """
        self.ypr_indicators.update(ypr)
        self.horizon.update(ypr[1])
        self.level.update(ypr[2])



class RollRuler:
    def __init__(self, navball_canvas, scale, angles, angles_subscale):
        self.canvas = navball_canvas
        self.scale = scale
        self.w, self.h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
        
        self.canvas.create_arc(
            self.w / 2 - self.scale, self.h / 2 - self.scale,
            self.w / 2 + self.scale, self.h / 2 + self.scale,
            start=np.min(angles), 
            extent=np.max(angles) - np.min(angles), 
            style=tk.ARC, 
            outline="white",
            width=3
        )

        bar_template = np.array([(0.9, 0),(1, 0)])
        bar_template_subs = np.array([(0.95, 0),(1, 0)])

        self._add_ruler(bar_template, angles)
        self._add_ruler(bar_template_subs, angles_subscale)
        

    def _add_ruler(self, template, angles) -> None:
        for angle in angles:
            theta = np.deg2rad(angle)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array([[c, -s], [s, c]])
            bar_template_rot = np.dot(self.scale * template, R)
            self.canvas.create_line(
                *bar_template_rot[0] + [self.w / 2, self.h / 2],
                *bar_template_rot[1] + [self.w / 2, self.h / 2],
                fill="white", 
                width=3,
                capstyle = tk.ROUND,
            )



class YPR_indicator:
    def __init__(self, navball_canvas, pos, v_space):
        self.canvas = navball_canvas
        self.titles = ['Yaw', 'Pitch', 'Roll']
        self.indicators = []
        for index, i in enumerate(self.titles):
            indicator = tk.Label(
                self.canvas, 
                text=f"{i}\t----", 
                font=(mainFont, 12),
                fg="white",
                bg="black",
            )
            indicator.place(
                x=pos[0], 
                y=pos[1] + index * v_space
            )
            self.indicators.append(indicator)

    def update(self, ypr) -> None:
        for axis, i, t in zip(ypr, self.indicators, self.titles):
            i.config(text=f"{t}\t{axis:.1f}")



class Horizon:
    def __init__(self, navball_canvas, bar_width: int | float, scale: int | float):
        self.canvas = navball_canvas
        self.w, self.h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()
        self.scale = scale # grad/px
        self.bar_width = bar_width
        self.text_gap = 5
        grad_step = 10
        minor_to_major_ratio = 0.66

        self.ground = self.canvas.create_rectangle(
            0, self.h / 2,
            self.w, 180 * self.scale, 
            fill = "#4C2F27"
        )

        self.right_end = (self.w - self.bar_width) / 2
        self.left_end = (self.w + self.bar_width) / 2
        self.right_end_minor = (self.w - self.bar_width * minor_to_major_ratio) / 2
        self.left_end_minor = (self.w + self.bar_width * minor_to_major_ratio) / 2

        self.bars_info = []
        bars = np.arange(-90, 90 + grad_step, grad_step)
        for alpha, next_alpha in zip(bars, bars[1:]):
            major_level = self.h / 2 - self.scale * alpha
            minor_level = self.h / 2 - self.scale * (alpha + next_alpha) / 2

            # Линии
            major_line = self.canvas.create_line(
                self.right_end, major_level,
                self.left_end, major_level,
                fill="white", 
                width=3,
                capstyle = tk.ROUND,
            )
            minor_line = self.canvas.create_line(
                self.right_end_minor, minor_level,
                self.left_end_minor, minor_level,
                fill="white", 
                width=2,
                capstyle = tk.ROUND,
            )
            
            # Создаем метки
            label_r = self.canvas.create_text(
                self.right_end - self.text_gap, major_level,
                text=f"{alpha}",
                font=(mainFont, 12),
                fill="white",
                anchor="e"
            )
            label_l = self.canvas.create_text(
                self.left_end + self.text_gap, major_level,
                text=f"{alpha}",
                font=(mainFont, 12),
                fill="white",
                anchor="w"
            )
            self.bars_info.append({
                'major_line': major_line,
                'minor_line': minor_line,
                'mark_r': label_r,
                'mark_l': label_l,
                'major_base': major_level,
                'minor_base': minor_level
            })


    def update(self, pitch: int | float) -> None:
        shift = self.scale * pitch
        self.canvas.moveto(self.ground, 0, self.h / 2 - shift)

        # Обновляем позиции линий
        for info in self.bars_info:
            new_major_level = info['major_base'] - shift
            new_minor_level = info['minor_base'] - shift
            self.canvas.coords(
                info['major_line'],
                self.left_end, new_major_level,
                self.right_end, new_major_level
            )
            self.canvas.coords(
                info['minor_line'],
                self.left_end_minor, new_minor_level,
                self.right_end_minor, new_minor_level
            )

            self.canvas.coords(
                info['mark_r'],
                self.right_end - self.text_gap, new_major_level
            )
            self.canvas.coords(
                info['mark_l'],
                self.left_end + self.text_gap, new_major_level
            )            



class Level:
    def __init__(self, navball_canvas, color: str, size: int | float):
        self.canvas = navball_canvas
        self.w, self.h = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()

        self.template = np.array([
            [-1, 0],
            [-1/4, 0],
            [0, 1/4],
            [1/4, 0],
            [1, 0]
        ])

        self.center_x = self.w / 2
        self.center_y = self.h / 2
        self.scaled_template = self.template * size

        # Инициализируем линии
        self.base_shape = []
        for p1, p2 in zip(self.scaled_template, self.scaled_template[1:]):
            line = self.canvas.create_line(
                *p1 + [self.center_x, self.center_y], 
                *p2 + [self.center_x, self.center_y],
                fill='black', 
                width=8,
                capstyle = tk.ROUND,
            )
            self.base_shape.append(line)
        self.shape = []
        for p1, p2 in zip(self.scaled_template, self.scaled_template[1:]):
            line = self.canvas.create_line(
                *p1 + [self.center_x, self.center_y], 
                *p2 + [self.center_x, self.center_y],
                fill=color, 
                width=4,
                capstyle = tk.ROUND,
            )
            self.shape.append(line)

        # Центральная точка
        point_size = 5
        point_base_size = 6
        self.canvas.create_oval(
            self.center_x - point_base_size, self.center_y - point_base_size, 
            self.center_x + point_base_size, self.center_y + point_base_size, 
            fill="black"
        )
        self.canvas.create_oval(
            self.center_x - point_size, self.center_y - point_size, 
            self.center_x + point_size, self.center_y + point_size, 
            fill=color
        )

    def update(self, roll: int | float) -> None:
        theta = np.deg2rad(roll)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s], [s, c]])
        rotated_shape = np.dot(self.scaled_template, R.T)
        
        for i, (base_line, line) in enumerate(zip(self.base_shape, self.shape)):
            x1, y1 = rotated_shape[i] + [self.center_x, self.center_y]
            x2, y2 = rotated_shape[i+1] + [self.center_x, self.center_y]
            self.canvas.coords(base_line, x1, y1, x2, y2)
            self.canvas.coords(line, x1, y1, x2, y2)








