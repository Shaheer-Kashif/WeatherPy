import requests
import json
from tkinter import *
from datetime import datetime
import pytz

# Main Tkinter Window
root = Tk()
root.title("WeatherPy")
root.iconbitmap("icons/weatherimage.ico")

# Accessing the API
api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/karachi?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
api = json.loads(api_req.content) 

# Getting Location from the Data
location = api['resolvedAddress']
location_label = Label(root,text = "Location: "+location)
location_label.pack()

# Today's Date
time_day = api['days'][0]['datetime']
time_day_label = Label(root,text = "Date: "+time_day)
time_day_label.pack()

# Today's Time
time = api['days'][0]['datetimeEpoch']
time_label = Label(root,text = "Time: "+str(time))
time_label.pack()

# Current Temperature
current_temp_f = api['days'][0]['temp']
current_temp_c = round(5/9 *(current_temp_f-32))
current_temp_label = Label(root,text = "Temperature: "+str(current_temp_c))
current_temp_label.pack()

root.mainloop()