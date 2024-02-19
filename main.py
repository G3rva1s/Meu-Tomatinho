import time
from time import strftime
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import matplotlib.pyplot as plt
import pygame as pyg
import sqlite3
from tkcalendar import*
from collections import defaultdict


#cores
red_bebe = '#FA8072'



class PomodoroTimer():

	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("620x450")
		self.root['bg'] = '#FA8072'
		self.root.title("Meu proprio tomatinho")
		self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file="tomato.png"))

		self.s = ttk.Style()
		self.s.configure('TNotebook.Tab', font=('Ubuntu', 16))
		self.s.configure('TButton', font=("Ubuntu", 16))
		#self.s.configure(bg = red_bebe)

		self.tabs = ttk.Notebook(self.root)
		self.tabs.pack(fill="both", pady=10, expand=True)


		self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
		self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
		self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
		self.tab4 = ttk.Frame(self.tabs, width=600, height=100)

		self.pomodoro_timer_label = ttk.Label(self.tab1, text='30:00', font=('Arial', 120))
		self.pomodoro_timer_label.pack(pady=20)	

		self.short_break_timer_label = ttk.Label(self.tab2, text='10:00', font=('Arial', 120))
		self.short_break_timer_label.pack(pady=20)

		self.long_break_timer_label = ttk.Label(self.tab3, text='20:00', font=('Arial', 120))
		self.long_break_timer_label.pack(pady=20)

		self.today_time = ttk.Label(self.tab4, 
									font = ('calibri', 48, 'bold'),
						            foreground = 'black')
		self.today_time.pack(pady=20)

		
		self.moment = Calendar()
		self.cal_label = ttk.Label(self.tab4, text=self.moment.get_date(),
								   font = ('calibri', 48, 'bold'))
		self.cal_label.pack(pady=10)
		

		self.grid_layout = ttk.Frame(self.root)
		self.grid_layout.pack(pady=10)
		
		self.start_button = ttk.Button(self.grid_layout, text="Start", command=lambda: 
			[self.start_timer_thread(), self.change_name_stop(), self.play()])
		self.start_button.grid(row=1, column=0)

		self.skip_button = ttk.Button(self.grid_layout, text='Skip', 
			command=self.skip_clock)
		self.skip_button.grid(row=1, column=1)

		self.reset_button = ttk.Button(self.grid_layout, text='Reset', 
			command=self.reset_clock)
		self.reset_button.grid(row=1, column=2)

		self.Stats_button = ttk.Button(self.grid_layout, text='Stats', 
			command=self.see)
		self.Stats_button.grid(row=2, column=1)

		self.Save_button = ttk.Button(self.grid_layout, text='Save', 
                              command=lambda: self.add_todays_pomod(self.moment.get_date()))
												#self.add_todays_pomod(self.moment.get_date())
												#self.add_todays_pomod(data, self.numero_de_pomodoros)

		self.Save_button.grid(row=2, column=0)


		self.tabs.add(self.tab1, text="Pomodoro")
		self.tabs.add(self.tab2, text="Pausa Curta")
		self.tabs.add(self.tab3, text="Pausa Longa")
		self.tabs.add(self.tab4, text="Dia")

		self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros hoje: 0", font=('Ubuntu', 16))
		self.pomodoro_counter_label.grid(row=3, column=0, columnspan=4, pady=10)


					
		def days(self):
			pass


		def time():
			string = strftime('%H:%M:%S %p')
			self.today_time.config(text = string)
			self.today_time.after(1000, time)
			

		self.numero_de_pomodoros = 0
		self.skipped = False
		self.stopped = False
		self.running = False

		self.pyg = pyg
		self.pyg.mixer.init()


		self.time = time
		self.time()


		self.root.mainloop()


	def start_timer_thread(self):
		if not self.running:
			t = threading.Thread(target=self.start_timer)
			t.start()
			self.running = True

	def change_name_stop(self):
		if self.start_button["text"] == "Start": 
			self.start_button.config(text = "Stop")
		else:
			self.start_button.config(text = "Start") 
			self.stopped = True
			self.running = False


	def start_timer(self):
		self.stopped = False

		self.skipped = False
		timer_id = self.tabs.index(self.tabs.select()) + 1
		self.play()

		if timer_id == 1:
			full_seconds = 60 * 30
			while full_seconds > 0 and not self.stopped:
				minutes, seconds = divmod(full_seconds, 60)
				self.pomodoro_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
				self.root.update()
				time.sleep(1)
				full_seconds -= 1

			if not self.stopped or self.skipped:
				self.numero_de_pomodoros += 1
				self.pomodoro_counter_label.config(text=f'Pomodoros: {self.numero_de_pomodoros:}')
				if self.numero_de_pomodoros % 4 == 0:
					self.tabs.select(2)
					self.start_timer()
				else:
					self.tabs.select(1)
				self.start_timer()
			
		elif timer_id == 2:
			full_seconds = 60 * 10
			while full_seconds > 0 and not self.stopped:
				minutes, seconds = divmod(full_seconds, 60)
				self.short_break_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
				self.root.update()
				time.sleep(1)
				full_seconds -= 1
			if not self.stopped or self.skipped:
				self.tabs.select(0)
				self.start_timer()
			
		elif timer_id == 3:
			full_seconds = 60 * 20
			while full_seconds > 0 and not self.stopped:
				minutes, seconds = divmod(full_seconds, 60)
				self.long_break_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
				self.root.update()
				time.sleep(1)
				full_seconds -= 1
			if not self.stopped or self.skipped:
				self.tabs.select(0)
				self.start_timer()

			else:
				print('fudeu!!!')


	def reset_clock(self):
		self.stopped = True
		self.skipped = False
		self.numero_de_pomodoros = 0
		self.pomodoro_timer_label.config(text="30:00")
		self.short_break_timer_label.config(text='10:00')
		self.long_break_timer_label.config(text='20:00')
		self.pomodoro_counter_label.config(text='Pomodoros: 0')
		self.running = False
		self.change_name_stop()


	def skip_clock(self):
		current_tab = self.tabs.index(self.tabs.select())
		if current_tab == 0:
			self.pomodoro_timer_label.config(text='30:00')
		elif current_tab == 1:
			self.short_break_timer_label.config(text='10:00')
		elif current_tab == 2:
			self.long_break_timer_label.config(text='20:00')


		self.stopped = True
		self.skipped = True

	def play(self):
		self.pyg.mixer.music.load("magic-ring.wav")
		self.pyg.mixer.music.play(loops=0)


	def today_is():
		pass

	def clock():
		pass


	def add_todays_pomod(self, data):
		

		data_formatada = data.strftime('%d/%m/%Y')

		conn = sqlite3.connect('molho_de_tomate.db')
		c = conn.cursor()
		c.execute("INSERT INTO pomodoros VALUES (?,?)", (data_formatada, self.numero_de_pomodoros))
		conn.commit()
		conn.close()

	def see(self):
		conn = sqlite3.connect('molho_de_tomate.db')
		c = conn.cursor()

		c.execute("SELECT * FROM pomodoros")
		
		items = c.fetchall()
		
		pomodoros_por_dia = defaultdict(int)

		for item in items:
			data = item[0]
			pomodoros = item[1]

			pomodoros_por_dia[data] += pomodoros

		dates = list(pomodoros_por_dia.keys())
		total_pomodoros = list(pomodoros_por_dia.values())
			

		plt.plot(dates, total_pomodoros)
		plt.xlabel('Dia')
		plt.ylabel('Nº Pomos')
		plt.title('try again')

		plt.show()

		conn.commit()
		conn.close()

PomodoroTimer()


