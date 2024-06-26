from tkinter import *
import threading
import time
from random import randint

root = Tk()
root.title("bleh")
root.geometry("500x400")

def five_sec():
    time.sleep(5)
    my_label.config(text="5 sec is up")


def rando():
    random_label.config(text=f"random number is {randint(0,100)}")
    my_label.config(text="balls")

my_label = Label(root, text="balls")
my_label.pack(pady=20)

start_button = Button(root, text = "Start recording", command=threading.Thread(target=five_sec).start)
start_button.pack(pady=20)

random_button = Button(root, text = "Start recording", command=rando)
random_button.pack(pady=20)

random_label = Label(root, text='')
random_label.pack(pady=20)

root.mainloop()

