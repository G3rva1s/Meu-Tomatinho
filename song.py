import pygame
from tkinter import *


root = Tk()
root.title("alerme teste")
root.geometry("500x400")

pygame.mixer.init()

def play():
	pygame.mixer.music.load("magic-ring.wav")
	pygame.mixer.music.play(loops=0)

mybutton = Button(root, text="toque", font=('Arial', 36), command=play)
mybutton.pack(pady=20)


root.mainloop()