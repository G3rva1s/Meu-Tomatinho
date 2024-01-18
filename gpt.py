import tkinter as tk
from tkinter import messagebox
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Temporizador Pomodoro")

        self.time_left = 1500  # 25 minutos em segundos (1500 segundos)
        self.running = False

        self.label = tk.Label(self.master, text=self.format_time())
        self.label.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Iniciar", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.master, text="Parar", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_timer(self):
        if self.running:
            self.running = False

            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.running:
            self.time_left -= 1
            self.label.config(text=self.format_time())

            if self.time_left == 0:
                self.running = False
                messagebox.showinfo("Pomodoro Concluído", "Tempo Pomodoro concluído!")
                self.reset_timer()
            else:
                self.master.after(1000, self.update_timer)

    def reset_timer(self):
        self.time_left = 1500
        self.label.config(text=self.format_time())

    def format_time(self):
        minutes, seconds = divmod(self.time_left, 60)
        return f"{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    pomodoro_timer = PomodoroTimer(root)
    root.mainloop()
