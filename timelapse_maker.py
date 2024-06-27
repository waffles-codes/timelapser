from tkinter import *
from mss import mss, tools
import threading
import pyautogui
import time
import os
import cv2
from PIL import Image, ImageTk

#the purpose of this code is to keep pyautogui highlighted
#so it isn't accidentally deleted by any future edits
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

#program defaults
end = False # whether or not to stop the recording
running = False # wheter or not the recording is running
seconds_per_frame = 2 # default spf value
made_video = False # whether or not a video has been made during program runtime (for delete button)

#start
root = Tk()
root.title("Timelapse App") #title of the app
width = 1190
height = 625
root.geometry(f'{width}x{height}+350+200') #sets starting resolution width x height and position x + y
root.resizable(1,0)
root.grid_columnconfigure((0, 1), weight=0)
root.grid_rowconfigure((0), weight=0)

#creating left_frame
left_padding = 10
left_width = round(width/3.5)
left_height = round(height-305)
left_frame = Frame(root, width=left_width, height=left_height)
left_frame.grid(row=0, column=0, padx=left_padding, pady=left_padding)
left_frame.config(bg="#d3d3d3")
left_frame.grid_columnconfigure((0), weight=0)
left_frame.grid_rowconfigure((0,1), weight=0)

message = "This program creates a timelapse"
message_label = Label(left_frame, text=message)
message_label.grid(row=0, column=0, padx=10, pady=10)
root.geometry(f'{width + round(len(message)*4.55)}x625')

#creating right_frame
right_padding = 10
right_height = round(height-(right_padding*2.3))
right_width = round(right_height*(16/10))  # make display 16 by 10
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
toolbar.grid(row=1, column=0, padx=toolbar_padding, pady=(left_height - tool_height + toolbar_padding)/2)
toolbar.config(bg="#b3b3b3")
toolbar.grid_columnconfigure((0), weight=0)
toolbar.grid_rowconfigure((0,1,2,3,4), weight=0)

def start_rec():
    print('RUNNING START REC')
    global running
    global end
    global seconds_per_frame
    if (running == False):
        running = True
        end = False
        time.sleep(2) # give 2 seconds to close the timelapse app before starting to record
        final_img = Label(right_frame)
        if (not os.path.isdir("temp_storage")):
            os.mkdir("temp_storage")
        while (end == False):
            #not writing to storage version (FINAL)
            with mss() as sct:
                monitor = sct.monitors[0]
                grabbed_img = sct.grab(monitor)
            png = tools.to_png(grabbed_img.rgb, grabbed_img.size)
            img = Image.frombytes("RGB", grabbed_img.size, grabbed_img.bgra, "raw", "BGRX") # PIL
            img = img.convert('RGB')
            # output = f"temp_storage/{time.strftime('%m-%d-%Y %H-%M-%S')}.jpg" # human readable ver
            output = f"temp_storage/{time.time_ns()}.jpg"                       # deployment ver
            #if the time set is < 1 sec, the previous image will sometimes be overwritten (NO LONGER AN ISSUE)
            img.save(output)

            #resize image for display
            resized_img = img.resize((right_width-20, right_height-20), None, None) #use right_frame params to show image
            new_img = ImageTk.PhotoImage(resized_img)
            final_img.config(image=new_img)
            final_img.grid(row=0, column=0, padx=10, pady=10)

            #this checks for stop process every second during the frame delay
            int_spf = int(seconds_per_frame)
            for i in range(int_spf):
                if (end == True):
                    running = False # end the loop and set flags
                    print('STOPPED')
                    return
                time.sleep(1)
            remaining_time = seconds_per_frame - int_spf
            time.sleep(remaining_time)
        
        running = False #set flags in case they weren't set before
        print('STOPPED')
        
    else:
        message = "the rec is goin"
        message_label.config(textvariable=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print('The recording is already running')

def stop():
    global end
    global message_label
    end = True

    message = "Set end to true"
    message_label.config(text=message)
    message_label.grid(row=0, column=0, padx=10, pady=10)
    root.geometry(f'{width + 105}x625')
    print("Set end to true")

def make_video():
    # put turning into video code here
    global end
    global width
    global made_video
    global message_label
    if (end == True):
        image_folder = "temp_storage"
        video_name = f"{time.strftime('%m-%d-%Y %H-%M-%S')}.mp4"
        # video_name = f"{time.time_ns()}.mp4"

        images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, f_width, layers = frame.shape

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        video = cv2.VideoWriter(video_name, fourcc, 30, (f_width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()
        made_video = True
        message = "video has been created"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{(width + round(len(message)*4.69))}x625')  #no clue why this makes the window go berserk
        print("video made")
    else:
        message = "Stop the recording first"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("ERR: The recording hasn't been stopped")

def clean_temp():
    #   removal of temp_storage code
    global made_video
    global message_label
    if made_video == False:
        message = "ERR: Click clean temp again to delete."
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("Video has not been made yet, click clean temp again to delete.")
        made_video = True
        return

    if (os.path.isdir("temp_storage")):
        files = os.listdir("temp_storage")
        for file in files:
            os.remove(f"temp_storage/{file}")
        os.rmdir("temp_storage")
        message = "Successfully deleted temp_storage"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("Removed temp_storage and all its files")
    else:
        message = "temp_storage does not exist"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("temp_storage does not exist")


# this is to bypass the "threads can only be started once" error
def create_start_thread():
	return threading.Thread(target=start_rec)

def start_thread():
    global end
    global running
    global message_label
    if running == False:
        print("Starting thread")
        thread = create_start_thread()
        print(thread)
        thread.start()
    elif end == False:
        message = "The recording is already running"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("The recording is already running")

start_button = Button(toolbar, text="Start recording", command=start_thread)
start_button.grid(row=0, column=0, padx=10, pady=10)

stop_button = Button(toolbar, text="Stop", command=stop)
stop_button.grid(row=1, column=0, padx=10, pady=10)

video_button = Button(toolbar, text="Save video", command=make_video)
video_button.grid(row=2, column=0, padx=10, pady=10)

clean_button = Button(toolbar, text="Clean temp", command=clean_temp)
clean_button.grid(row=3, column=0, padx=10, pady=10)

change_fps = Entry(toolbar, borderwidth=2)
change_fps.insert(0, "Change seconds/frame")
change_fps.grid(row=4, column=0, padx=5, pady=10)

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def fps_changer():
    global seconds_per_frame
    global message_label
    temp_fps = change_fps.get()
    if is_float(temp_fps) and float(temp_fps) > 0:
        temp_fps = float(temp_fps)
        seconds_per_frame = temp_fps

        message = f"changed seconds_per_frame to {seconds_per_frame}"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print(f"changed seconds_per_frame to {seconds_per_frame}")
    else: 
        message = "enter a valid input please"
        message_label.config(text=message)
        message_label.grid(row=0, column=0, padx=10, pady=10)
        root.geometry(f'{width + round(len(message)*4.55)}x625')
        print("invalid input for change fps")

fps_button = Button(toolbar, text="<", command=fps_changer)
fps_button.grid(row=4, column=1, padx=5, pady=10)


root.mainloop()