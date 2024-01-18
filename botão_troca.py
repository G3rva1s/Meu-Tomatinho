from tkinter import *
 
# creating the tkinter window
Main_window = Tk()

def counter():
   
    if my_button['text'] == 'Start':
    	# configure 
    	my_button.config(text = "Stop")
    else:
    	my_button.config(text = "Start")

def oloko():
	pass



 
# create a button widget and attached   
# with counter function   
my_button = Button(Main_window, text = 'Start', command =lambda: [counter(), oloko()]) 
# place the widgets 
# in the gui window
my_button.pack()
 
# Start the GUI 
Main_window.mainloop()
