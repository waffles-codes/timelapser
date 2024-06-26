from tkinter import *
from mss import mss, tools
import pyautogui
import threading
import time
import os
from PIL import Image, ImageTk

root = Tk()
root.title("Timelapse App") #title of the app
width = 1190
height = 625
root.geometry(f'{width}x{height}+350+200') #sets starting resolution width x height and position x + y
root.resizable(0,0)

#creating left_frame
left_padding = 10
left_width = round(width/3.5)
left_height = round(height-(left_padding*3))
left_frame = Frame(root, width=left_width, height=left_height)
left_frame.grid(row=0, column=0, padx=left_padding, pady=left_padding)
left_frame.config(bg="#d3d3d3")

#creating right_frame
right_padding = 10
right_height = round(height-(right_padding*2.3))
right_width = round(right_height*(16/10))
right_frame = Frame(root, width=right_width, height=right_height)
right_frame.grid(row=0, column=1, padx=0, pady=right_padding)
right_frame.config(bg="#d3d3d3")

#experimenting with canvas
# canvas = Canvas(root, width=(width - width/3.5 - (10*3)), height=(height-(10*2)))
# canvas.grid(row=0, column=1, padx=0, pady=10)

#create toolbar in left_frame
toolbar_padding = 10
tool_width = left_width - left_padding*2
tool_height = 150
toolbar = Frame(left_frame, width=tool_width, height=tool_height) #specify in left_frame
toolbar.grid(row=0, column=0, padx=toolbar_padding, pady=(left_height - tool_height + toolbar_padding)/2)
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
        time.sleep(2) # give 2 seconds to close the timelapse app before starting to record
        if (not os.path.isdir("temp_storage")):
            os.mkdir("temp_storage")
        while (end == False):
            #screenshot --> convert version (OBSOLETE)
            # with mss() as sct:
            #     filename = sct.shot(mon=-1, output=f"temp_storage/{time.strftime('%m-%d-%Y %H-%M-%S')}.png")
            # print(filename) #prints file in png state
            # img = (Image.open(filename)) # PIL
            # rgb_img = img.convert('RGB')
            # rgb_img.save(f'{os.path.splitext(filename)[0]}.jpg')
            # os.remove(filename)
            # resized_img = rgb_img.resize((right_width-20, right_height-20), None, None) #use right_frame params to show image
            # new_img = ImageTk.PhotoImage(resized_img)
            # final_img = Label(right_frame, image=new_img)
            # final_img.grid(row=0, column=0, padx=10, pady=10)

            #not writing to storage version
            with mss() as sct:
                monitor = sct.monitors[0]
                grabbed_img = sct.grab(monitor)
            png = tools.to_png(grabbed_img.rgb, grabbed_img.size)
            img = Image.frombytes("RGB", grabbed_img.size, grabbed_img.bgra, "raw", "BGRX") # PIL
            img = img.convert('RGB')
            output = f"temp_storage/{time.strftime('%m-%d-%Y %H-%M-%S')}.jpg"
            img.save(output)

            #resize image for display
            resized_img = img.resize((right_width-20, right_height-20), None, None) #use right_frame params to show image
            new_img = ImageTk.PhotoImage(resized_img)
            final_img = Label(right_frame, image=new_img)
            final_img.grid(row=0, column=0, padx=10, pady=10)

            time.sleep(2) # sets fps, figure out how to stop process while sleeping IMPORTANT
        running = False
        print('STOPPED')
        
    else:
        print('The recording is already running')

def stop():
    global end
    end = True
    print("Set end to true")
    # put turning into video code here

    #   removal code (will need to be implemented eventually)
    # if (os.path.isdir("temp_storage")):
    #     files = os.listdir("temp_storage")
    #     for file in files:
    #         os.remove(f"temp_storage/{file}")
    #     os.rmdir("temp_storage")
    #     print("Removed temp_storage and all its files")

start_button = Button(toolbar, text="Start recording", command=threading.Thread(target=start_rec).start)
start_button.grid(row=1, column=0, padx=10, pady=10)

stop_button = Button(toolbar, text="Stop", command=stop)
stop_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()