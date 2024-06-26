from tkinter import *
from mss import mss, tools
import cv2
import threading
import time
from PIL import Image, ImageTk

root = Tk()
root.title("Timelapse App") #title of the app
width = 768
height = 432
# root.minsize(width, height)
# root.maxsize(width, height)
# root.geometry(f'350+200') #sets starting resolution width x height and position x + y

#creating left_frame
left_padding = 10
left_width = (width/3.5)
left_height = height-(left_padding*2)
left_frame = Frame(root, width=left_width, height=left_height)
left_frame.grid(row=0, column=0, padx=left_padding, pady=left_padding)
left_frame.config(bg="#d3d3d3")

#creating right_frame
right_padding = 10
right_width = (width - width/3.5 - (right_padding*3))
right_height = (height-(right_padding*2))
right_frame = Frame(root, width=right_width, height=right_height)
right_frame.grid(row=0, column=1, padx=0, pady=right_padding)
right_frame.config(bg="#d3d3d3")
canvas = Canvas(right_frame, width=right_width-right_padding, height=right_height-right_padding)

#create text in left_frame
display_text = Label(left_frame, text="This is an app for creating a timelapse")
display_text.grid(row=0, column=0, padx=10, pady=10)

# #create text in right_frame
# display_text = Label(right_frame, text="The images will show up here")
# display_text.grid(row=0, column=0, padx=10, pady=10)

#create toolbar in left_frame
toolbar_padding = 10
tool_width = left_width - left_padding*2
tool_height = 150
toolbar = Frame(left_frame, width=tool_width, height=tool_height) #specify in left_frame
toolbar.grid(row=1, column=0, padx=toolbar_padding, pady=(left_height - tool_height + toolbar_padding)/2)
toolbar.config(bg="#b3b3b3")

end = False # this controls the screenshot loop
running = False # this determines whether or not we can call screenshot loop when we press start

def start_rec():
    print('RUNNING START REC')
    global running
    global end
    if (running == False):
        running = True
        end = False
        time.sleep(1) # give 1 second to close the timelapse app before starting
        while (end == False):
            with mss() as sct:
                filename = sct.shot(mon=-1, output="output.png") # this should create a new folder before taking more screenshots
            print(filename)
            # img = (Image.open(filename)) # PIL
            # resized_img = img.resize((640, 400), None, None)
            # new_img = ImageTk.PhotoImage(resized_img)
            # final_img = Label(right_frame, image=new_img)
            # final_img.grid(row=0, column=0, padx=10, pady=10)
            time.sleep(1) # 1 fps, could be lower but would have to figure out how to instantly kill the process
        running = False
        print('STOPPED')
        
    else:
        print('The recording is already running')

def stop():
    global end
    end = True
    print("Set end to true")
    # put turning into video code here


start_button = Button(toolbar, text="Start recording", command=threading.Thread(target=start_rec).start)
start_button.grid(row=1, column=0, padx=10, pady=10)

stop_button = Button(toolbar, text="Stop", command=stop)
stop_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()