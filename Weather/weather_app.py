from tkinter import *
import requests
import api_key
import icons
import random
import five_day
import hourly

root = Tk()
root.wm_title("Window Title") #Makes the title that will appear in the top left
root.config(bg = "#00a2ff")

#root.attributes("-fullscreen", True)
root.geometry("800x480")
w = 800
h = 480

fw = w/2 - 10
fh = h - 10

#Left Frame and its contents
leftFrame = Frame(root, width = fw, height = fh, bg="#C8F9C4", highlightthickness=2, highlightbackground="#111")
leftFrame.grid(row=0, column=0, padx=7, pady=5, sticky=N+S) 

day_pady = 8
day_h = (fh - 3*day_pady)/2 - 1

day_padx = 8
day_w = (fw - 2*day_padx)/1 - 1

daily = Frame(leftFrame, width=fw - 20, height = day_h, bg="#0055de",  highlightthickness=1, highlightbackground="#333")
daily.grid(row=0, column=0, padx=day_padx, pady=day_pady)

today = Label(daily, text="30°C", bg="#0055de", takefocus=0, foreground="#fff", font=("Arial", 54))

today_h = today.winfo_reqheight()
today_pad = (day_h - today_h)/2

weather = "sunny"

today_w = today.winfo_reqwidth()
today_image = icons.icons(root, daily, 1, weather, 8)
daily.columnconfigure(1, weight=1) 

today_wpad = (day_w - today_w - today_image.width)/3

today.grid(row=0, column=0, padx=today_wpad, pady=today_pad, sticky=E)

daily1 = Frame(leftFrame, width=fw - 20, height = day_h, bg="#0055de",  highlightthickness=1, highlightbackground="#333")
daily1.grid(row=1, column=0, padx=8, pady=0)

hour0 = hourly.hourlyForecast(root, "1:00", 0, daily1, day_h, fw - 20, weather, True)
hour1 = hourly.hourlyForecast(root, "2:00", 1, daily1, day_h, fw - 20, weather, False)
hour2 = hourly.hourlyForecast(root, "3:00", 2, daily1, day_h, fw - 20, weather, True)
hour3 = hourly.hourlyForecast(root, "4:00", 3, daily1, day_h, fw - 20, weather, False)
hour4 = hourly.hourlyForecast(root, "5:00", 4, daily1, day_h, fw - 20, weather, True)

#Right Frame and its contents
rightFrame = Frame(root, width=fw, height = fh, bg="#C8F9C4", highlightthickness=2, highlightbackground="#111")
rightFrame.grid(row=0, column=1, padx=0, pady=5, sticky=N+S)

day0 = five_day.dailyForecast(root, "Monday", 0, rightFrame, fh, fw, weather, True)
day1 = five_day.dailyForecast(root, "Tuesday", 1, rightFrame, fh, fw, weather, False)
day2 = five_day.dailyForecast(root, "Wednesday", 2, rightFrame, fh, fw, weather, True)
day3 = five_day.dailyForecast(root, "Thursday", 3, rightFrame, fh, fw, weather, False)
day4 = five_day.dailyForecast(root, "Friday", 4, rightFrame, fh, fw, weather, True)

for frame in [rightFrame, leftFrame, daily, today, daily1]:
    frame.grid_propagate(False)

UserAgent = (api_key.Project, api_key.Email)
lat = 40
lon = 75

def update_today(label):
    current_data = requests.get(f'https://api.weather.gov/gridpoints/PHI/{lat},{lon}/forecast').json()
    temperature = current_data['properties']['periods'][0]['temperature']
    
    label.configure(text=f'{temperature}°F')
    label.after(3600000, update_today, label)

def update_days(labels):
    for label in labels:
        rand = round(random.random()*50-9)
        label.day_temp.configure(text=f'Hi: {rand}°C | Lo: {rand/2}°C')
    
    labels[0].day_temp.after(1000, update_days, labels)

def update_hours(labels):
    for label in labels:
        rand = round(random.random()*50-9)
        label.day_temp.configure(text=f'Hi: {rand}°C | Lo: {rand/2}°C')
    
    labels[0].day_temp.after(3600000, update_hours, labels)

update_today(today)
update_days([day0, day1, day2, day3, day4])
update_hours([hour0, hour1, hour2, hour3, hour4])

current_data = requests.get(f'https://api.weather.gov/gridpoints/PHI/{lat},{lon}/forecast').text

file = open("data.txt", "w")
file.write(current_data)
file.close()

mainloop()