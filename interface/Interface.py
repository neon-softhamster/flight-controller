import threading
import queue
import tkinter as tk
from styles.Style import *
from backend.Communicatior import Communicator
from interface.widgets.Joy_indicator import Joystic_indicator
from interface.widgets.Infos import InfoBar
from interface.widgets.NavBall import NavBall



class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI controller v0.1")
        self.root.attributes('-fullscreen', True)
        # self.root.geometry("1920x1080")

        # Escape to exit
        self.root.bind('<Escape>', self.on_closing)
        
        # Запуск бэкенда в отдельном потоке
        self.backend_queue = queue.Queue()
        self.com = Communicator(self.backend_queue)
        
        # Добавляем флаг успешной инициализации
        self.initialized = False
        
        if self.com.self_check():
            self.stop_backend_event = threading.Event()
            self.backend_thread = threading.Thread(
                target=self.com.run,
                args=(self.stop_backend_event,)
            )
            self.backend_thread.daemon = True
            self.backend_thread.start()
            self.initialized = True
            self.create_widgets()
            self.update_ui()
        else:
            self.root.after(100, self.root.destroy)


    def create_widgets(self):
        """ Создает элементы интерфейса """
        self.master_canvas = tk.Canvas(bg="black", width=1920, height=1080)
        self.master_canvas.pack(fill=tk.BOTH, expand=True)

        # визуальное разделение окна на зоны
        self.master_canvas.create_line(0, 640, 1920, 640, fill="grey", width=2)  # Горизонтальная
        self.master_canvas.create_line(640, 0, 640, 640, fill="grey", width=2)  # Вертикальная
        self.master_canvas.create_line(1280, 0, 1280, 640, fill="grey", width=2)  # Вертикальная

        self.joy_indicatior = Joystic_indicator(self.master_canvas, (500, 500))
        self.master_canvas.create_window(320, 320, window=self.joy_indicatior.main, anchor="center")
        self.info_bar = InfoBar(self.master_canvas)
        
        self.nav_ball = NavBall(self.master_canvas, (500, 500))
        self.master_canvas.create_window(960, 320, window=self.nav_ball.main, anchor="center")


    def update_ui(self):
        """ Обновляет элементы UI """
        try:
            # Проверяем новые данные в очереди
            while not self.backend_queue.empty():
                com, tele, conf = self.backend_queue.get_nowait()

                self.joy_indicatior.update(self.master_canvas, com)

                if tele['status'] == "Ok":
                    self.nav_ball.update([tele['yaw'], tele['pitch'], tele['roll']])
        
        except queue.Empty:
            pass
        
        # Планируем следующее обновление
        self.root.after(50, self.update_ui)


    def on_closing(self, event=None):
        self.stop_backend_event.set()
            
        # Ожидаем завершения потока (максимум 1 секунду)
        if self.backend_thread.is_alive():
            self.backend_thread.join(timeout=1.0)

        self.root.destroy()