from interface.Interface import Interface
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    # Устанавливаем обработчик закрытия только если инициализация прошла успешно
    if app.initialized:
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    else:
        root.destroy()
    root.mainloop()