import tkinter as tk

class Joystic_indicator:
    def __init__(self, master_canvas, size):
        self.w, self.h = size
        self.mark_size = 10
        self.cross_size = (self.w + self.h) / 2 * 0.8

        self.main = tk.Canvas(
            master_canvas, 
            width=self.w, 
            height=self.h, 
            bg="grey23"
        )

        # прекрестье
        self.main.create_line(
            (self.w - self.cross_size) / 2, self.h / 2, 
            (self.w + self.cross_size) / 2, self.h / 2, 
            fill="white", 
            width=3
        )
        self.main.create_line(
            self.w / 2, (self.h - self.cross_size) / 2, 
            self.w / 2, (self.h + self.cross_size) / 2, 
            fill="white", 
            width=3
        )

        self.pt_trim = self.main.create_oval(
            (self.w - self.cross_size) / 2, (self.h - self.cross_size) / 2, 
            (self.w + self.cross_size) / 2, (self.h + self.cross_size) / 2, 
            fill="yellow"
        )
        self.pt_no_trim = self.main.create_oval(
            (self.w - self.cross_size) / 2, (self.h - self.cross_size) / 2, 
            (self.w + self.cross_size) / 2, (self.h + self.cross_size) / 2, 
            fill="white"
        )

    def update(self, master, command):
        no_trim, trim = command
        self.main.coords(
            self.pt_trim, 
            self.cross_size / 2 * (trim[0] - 90) / 90 - 5 + self.w / 2, 
            self.cross_size / 2 * (trim[1] - 90) / 90 - 5 + self.h / 2, 
            self.cross_size / 2 * (trim[0] - 90) / 90 + 5 + self.w / 2, 
            self.cross_size / 2 * (trim[1] - 90) / 90 + 5 + self.h / 2, 
        )
        self.main.coords(
            self.pt_no_trim, 
            self.cross_size / 2 * (no_trim[0] - 90) / 90 - 5 + self.w / 2, 
            self.cross_size / 2 * (no_trim[1] - 90) / 90 - 5 + self.h / 2, 
            self.cross_size / 2 * (no_trim[0] - 90) / 90 + 5 + self.w / 2, 
            self.cross_size / 2 * (no_trim[1] - 90) / 90 + 5 + self.h / 2, 
        )