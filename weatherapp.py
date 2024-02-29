import requests, json, datetime, time, threading
from tkinter import *
from PIL import ImageTk,Image

# Main Tkinter Window
root = Tk()
root.title("WeatherPy")
root.iconbitmap("icons/weatherimage.ico")
root.configure(bg = "white")

# Defining Weather Icon Images
sunny = ImageTk.PhotoImage(Image.open("icons/sun.png"))
cloudy = ImageTk.PhotoImage(Image.open("icons/cloudy.png"))
rain = ImageTk.PhotoImage(Image.open("icons/rain.png"))


# Accessing the API
api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/karachi?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
api = json.loads(api_req.content) 

# Getting Location from the Data
location = api['resolvedAddress']
location_label = Label(root,text = "Location: "+location)
location_label.grid(row=5,column=0)

# Today's Date
time_day = api['days'][0]['datetime']
time_day_label = Label(root,text = "Date: "+time_day)
time_day_label.grid(row=4,column=0)

# Today's Time
def time_update(time_offset):
    
    # Loop for Updating Time
    while True:
        
        # Getting Current Time in Epoch Format
        time_epoch = time.time()
        
        # Converting to Readable Format
        real_time = datetime.datetime.utcfromtimestamp(time_epoch)
        
        # Checking the Time Zone Offset is in Decimal or not and setting the time according to that
        if time_offset == int(time_offset):
            time_to_add = datetime.timedelta(hours=time_offset, minutes=0, seconds=0)
        else:
            decimal_part = time_offset % 1
            time_to_add = datetime.timedelta(hours=int(time_offset), minutes=decimal_part*60, seconds=0)
        
        # Adding the Offset and GMT Time to get Final Time
        new_time = real_time + time_to_add
        
        # Adding the Offset and GMT Time to get Final Time
        new_time = new_time.strftime('%H:%M:%S')
        
        time_label = Label(root,text = "Time: "+str(new_time))
        time_label.grid(row=3,column=0)
        
        time.sleep(1)

# Time Offset
time_off = api['tzoffset']

# Creating Different Thread for Time
time_thread = threading.Thread(target=time_update, args=(time_off,))
time_thread.daemon = True
time_thread.start()

# Current Temperature
current_temp_f = api['days'][0]['temp']
current_temp_c = round(5/9 *(current_temp_f-32))
current_temp_label = Label(root,text = "Temperature: "+str(current_temp_c))
current_temp_label.grid(row=2,column=0)

# Weather Icon based on Conditions
condition = api['days'][0]['conditions']
if 'CLEAR' in condition.upper():
    img_label = Label(image=sunny)
elif 'CLOUDY' in condition.upper():
    img_label = Label(image=cloudy)
elif 'RAIN' in condition.upper():
    img_label = Label(image=rain)

img_label.grid(row=0,column=0)

# Weather Description
desc = api['days'][0]['description']
desc_label = Label(root,text = desc)
desc_label.grid(row=1,column=0)

root.mainloop()