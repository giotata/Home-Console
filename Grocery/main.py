import tkinter as tk
from tkinter import *
from datetime import datetime
import pyautogui
import threading

import firebase_admin
from firebase_admin import storage
from firebase_admin import firestore
from firebase_admin.firestore import SERVER_TIMESTAMP

cred = firebase_admin.credentials.Certificate(r'C:\Local_Code\Home-Console\Grocery\cred.json')
default_app = firebase_admin.initialize_app(cred, {
	'storageBucket':'grocerylist-b8759.appspot.com'
})

bucket = storage.bucket()
db = firestore.client()
time_ref = db.collection("Timestamps").document("Timestamp")

# Define a custom event
custom_signal_event = threading.Event()

# Define a handler function for the custom signal
def custom_signal_handler():
    before = datetime.now().timestamp()

    write = False
    while True:
        now = datetime.now().timestamp()
        
        if(write and ((now - before)>1)):
            print("Taking screenshot.")
            image1 = pyautogui.screenshot("image1.png")
            write = False
            before = datetime.now().timestamp()

            blob = bucket.blob('image1.png')
            blob.upload_from_filename('image1.png')

            time_ref.set({"Time" : SERVER_TIMESTAMP})

        # Wait for the event to be set
        update = custom_signal_event.wait(0.1)
        if(update):
            write = True
            before = datetime.now().timestamp()
        # Reset the event
        custom_signal_event.clear()

# Start a thread to handle the custom signal
handler_thread = threading.Thread(target=custom_signal_handler)
handler_thread.daemon = True  # Allows the thread to exit when the main program exits
handler_thread.start()


color = 'black'
on = True
prev_x = 0
prev_y = 0

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Canvas")
        
        self.canvas = tk.Canvas(self.root, bg="white", width=1920, height=1080)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.start)
        self.canvas.bind("<ButtonRelease-1>", self.end) 
        
    def start(self, event):
        global writing
        writing = True
        global prev_x, prev_y
        prev_x, prev_y = event.x, event.y

    def end(self, event):
        global writing
        writing = False
        custom_signal_event.set()

    def roundline(self, start_x, start_y, end_x, end_y, size=1):
        Xaxis = end_x-start_x
        Yaxis = end_y-start_y
        dist = max(abs(Xaxis), abs(Yaxis))

        for i in range(dist):
            x = int(start_x+float(i)/dist*Xaxis)
            y = int(start_y+float(i)/dist*Yaxis)
            x1, x2 = (x - size), (x + size)
            y1, y2 = (y - size), (y + size)

            self.canvas.create_oval(x1, y1, x2, y2, fill='black', outline='black', width=2)

    def paint(self, event):
        global color
        global prev_x, prev_y
       
        if(writing):
            self.roundline(prev_x, prev_y, event.x, event.y)

            prev_x, prev_y = event.x, event.y

def black_clicked():
    global color
    color = "black"
    print("black")
def red_clicked():
    global color
    color = "red"
    print("red")
def blue_clicked():
    global color 
    color = "blue"
    print("blue")
def green_clicked():
    global color
    color = "green"
    print("green")
def erase_clicked():
    global color
    color = "white"
    print("erase")
def exit_clicked():
    quit()

button_positions = [(10, 10), (110, 10), (210, 10), (310, 10), (410, 10)]

def show_button(buttons):
    global on
    global button_positions

    if(on):
        for button in buttons:
            button.place_forget()
        on = False
    else:
        for button, (x, y) in zip(buttons, button_positions):
            button.place(x=x, y=y)
        on = True        
        
if __name__ == "__main__":
    root = tk.Tk()
    
    app = DrawApp(root)
    black = Button(root, text='', width=10, activebackground='white',
             height=2, bd='10',bg='black', command=black_clicked)
    black.place(x=10, y=10)
    red = Button(root, text='', width=10, activebackground='white',
             height=2, bd='10',bg='red', command=red_clicked)
    red.place(x=110, y=10)
    blue = Button(root, text='', width=10, activebackground='white',
             height=2, bd='10',bg='blue', command=blue_clicked)
    blue.place(x=210, y=10)
    green = Button(root, text='', width=10, activebackground='white',
             height=2, bd='10',bg='green', command=green_clicked)
    green.place(x=310, y=10)
    erase = Button(root, text='ERASE', width=10, activebackground='white',
             height=2, bd='10',bg='white', command=erase_clicked)
    erase.place(x=410, y=10)

    mid = root.winfo_screenwidth()/2
    left = root.winfo_screenwidth() - 110
    bottom = root.winfo_screenheight() - 70

    button_positions.append((left, 10))

    exit = Button(root, text='X', width=10, activebackground='white',
             height=2, bd='10',bg='red', command=exit_clicked)
    exit.place(x=left, y=10)

    show_hide = Button(root, text='Show/Hide', width=10, activebackground='black', fg = 'white',
             height=1, bd='10',bg='black', command=lambda: show_button([black, red, blue, green, erase, exit]))
    show_hide.place(x=left, y=bottom)

    root.attributes("-fullscreen", True)
    root.mainloop()