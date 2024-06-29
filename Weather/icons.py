from tkinter import *

class icons:
    def __init__(self, root, frame, col, weather, downscale):
        self.root = root
        self.frame = frame

        self.image = PhotoImage(file = 'Weather/sun.png')
        self.smaller_image = self.image.subsample(downscale, downscale)

        self.width, self.height = self.smaller_image.width(), self.smaller_image.height()
        self.canvas = Canvas(self.frame, bg="#0055de", width=self.width, height=self.height, highlightthickness=0)

        self.canvas.grid(row=0, column=col, padx=10, pady=0, sticky='e')
        self.canvas.create_image(0, 0, image=self.smaller_image, anchor='nw')