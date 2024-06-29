from tkinter import *
import icons

class hourlyForecast:
    def __init__(self, root, day, row, frame, container_h, container_w, daily_weather, pady):
        if(pady):
            self.pady = 4
        else:
            self.pady = 0

        self.h = (container_h - 6*4)/5
        self.w = container_w - 10

        self.widget = Frame(frame, width=self.w, height = self.h, bg="#0055de",  highlightthickness=1, highlightbackground="#333")
        self.widget.grid(row=row, column=0, padx=4, pady=self.pady)

        self.day = Label(self.widget, text=f"{day}", bg="#0055de", takefocus=0, foreground="#fff", font=("Arial", 12))
        self.day_temp = Label(self.widget, text="Hi: 30°C | Lo: 0°C", bg="#0055de", takefocus=0, foreground="#fff", font=("Arial", 12))
        self.day_image = icons.icons(root, self.widget, 2, daily_weather, 30)
        self.widget.columnconfigure(1, weight=1)
        self.widget.columnconfigure(2, weight=1)

        self.day_h = self.day.winfo_reqheight()
        self.day_ypad = (self.h - self.day_h)/2

        self.day_w = self.day.winfo_reqheight()
        self.temp_w = self.day_temp.winfo_reqheight()
        self.day_wpad = (self.w - self.day_w - self.temp_w - self.day_image.width)/4

        self.day.grid(row=0, column=0, padx=10, pady=self.day_ypad, sticky=E)
        self.day_temp.grid(row=0, column=1, padx=10, pady=self.day_ypad, sticky=E)

        self.widget.grid_propagate(False)