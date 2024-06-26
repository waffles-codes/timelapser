from tkinter import *
import asyncio
from mss import mss

root = Tk()
root.title("Timelapse App") #title of the app
width = 768
height = 432
root.minsize(width, height)
root.maxsize(width, height)
root.geometry(f'{width}x{height}+350+200') #sets starting resolution width x height and position x + y

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

#create text in left_frame
display_text = Label(left_frame, text="This is an app for creating a timelapse")
display_text.grid(row=0, column=0, padx=10, pady=10)

#create text in right_frame
display_text = Label(right_frame, text="The images will show up here")
display_text.grid(row=0, column=0, padx=10, pady=10)

#create toolbar in left_frame
toolbar_padding = 10
tool_width = left_width - left_padding*2
tool_height = 150
toolbar = Frame(left_frame, width=tool_width, height=tool_height) #specify in left_frame
toolbar.grid(row=1, column=0, padx=toolbar_padding, pady=(left_height - tool_height + toolbar_padding)/2)
toolbar.config(bg="#b3b3b3")

end = False
running = False

def start():
    if (running == False):
        screenshot_loop()
    else:
        running = True
        
async def screenshot_loop():
    end = False
    await asyncio.sleep(1) # give 1 second to close the timelapse app before starting
    while(end == False):
        filename = mss().shot()
        print(filename)
        image = PhotoImage(file=filename)
        img = Label(right_frame, image=image)
        img.grid(row=0, column=0, padx=10, pady=10)
        await asyncio.sleep(30) # sleep for 30 seconds on an async process

def stop():
    end = True

start = Button(toolbar, text="Start recording", command=start)
start.grid(row=1, column=0, padx=10, pady=10)

stop = Button(toolbar, text="Stop", command=stop)
stop.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()