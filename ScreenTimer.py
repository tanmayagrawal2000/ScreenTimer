from tkinter import *
from PIL import ImageGrab, ImageChops
import time
global topleftx
global toplefty
global bottomrightx
global bottomrighty
a =[]
t =[]
root = Tk()

def start_stopwatch():
    global start_time
    getscreenspecs()
    root.state(newstate='iconic')
    time.sleep(2)
    start_time = time.time()
    root.after(10, update_stopwatch)
    
def getscreenspecs():
    global a
    width = root.winfo_width()
    height = root.winfo_height()
    x = root.winfo_x()
    y = root.winfo_y()
    root.state(newstate='iconic')
    time.sleep(1)
    temp_time = time.localtime()
    t.append(temp_time)
    topleftx = x + 10
    toplefty = y
    bottomrightx = width + topleftx
    bottomrighty = height + toplefty
    im2 = ImageGrab.grab(bbox=(topleftx,toplefty,bottomrightx,bottomrighty))
    a = [topleftx,toplefty,bottomrightx,bottomrighty]
    #im2.show()
    #print("Window size: {}x{}".format(width, height))
    #print("Window position: {}x{}".format(x, y))
    
def update_stopwatch():
    global start_time
    if start_time:
        # Calculate the elapsed time
        elapsed = round(time.time() - start_time, 2)
        
        # Update the label with the elapsed time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        #time_label.config(text=time_str)
        
        # Check if the screen has changed
        if screen_changed():
            stop_stopwatch()
        else:
            root.after(10, update_stopwatch)
            
def stop_stopwatch():
    global stop_time, elapsed_time
    stop_time = time.time()
    elapsed_time = round(stop_time - start_time, 2)
    root.quit()

def screen_changed():
    global last_image
    # Capture the screen
    image = ImageGrab.grab(bbox = (a[0], a[1], a[2], a[3]))
    #image.show()
    
    # Compare the current image with the previous image
    if last_image is not None:
        diff = ImageChops.difference(image, last_image)
        if diff.getbbox():
            final_temp_time = time.localtime()
            t.append(final_temp_time)
            # The screen has changed
            return True
    
    # Save the current image for the next comparison
    last_image = image
    return False


# Set window size and position
root.geometry("400x300+100+100")

start_button = Button(root, text="Start", font=("Helvetica", 15), command= start_stopwatch)
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)
last_image = None
root.mainloop()
start_hour = int(time.strftime("%H", t[0]))
start_minute = int(time.strftime("%M", t[0]))
start_secs = int(time.strftime("%S", t[0]))
end_hour = int(time.strftime("%H", t[1]))
end_minute = int(time.strftime("%M", t[1]))
end_secs = int(time.strftime("%S", t[1]))
time1_sec = start_hour*3600 + start_minute*60 + start_secs
time2_sec = end_hour*3600 + end_minute*60 + end_secs
diff_sec = abs(time1_sec - time2_sec)
hour_diff = diff_sec // 3600
min_diff = (diff_sec % 3600) // 60
sec_diff = (diff_sec % 3600) % 60
print(f"Time difference: {hour_diff} hours {min_diff} minutes {sec_diff} seconds")



