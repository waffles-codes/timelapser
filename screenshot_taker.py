import time
import os
from tkinter import *
from mss import mss

root = Tk()
root.title("Timelapse App") #title of the app
root.minsize(300, 200)
root.maxsize(300, 200)
root.geometry("300x200+570+350") #sets starting resolution 300x200 and position x+y

display_text = Label(root, text="This is an app for creating a timelapse")
display_text.pack()  #this packs the text into the window

root.mainloop()


# with mss() as sct:
#     filename = sct.shot()

# print(filename)