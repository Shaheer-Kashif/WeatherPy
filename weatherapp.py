import requests, json, datetime, time, threading
from tkinter import *
from PIL import ImageTk,Image

# Main Tkinter Window
root = Tk()
root.title("WeatherPy")
root.iconbitmap("icons/weatherimage.ico")
root.configure(bg = "white")
root.option_add('*background', 'white')

# Defining Weather Icon Images
sunny = Image.open("icons/sun.png")
cloudy_day = Image.open("icons/cloudy.png")
rain_day = Image.open("icons/rain.png")
night = Image.open("icons/night.png")
cloudy_night = Image.open("icons/cloudy-night.png")
rain_night = Image.open("icons/rainy-night.png")

# Resizing Images to Make it Small
images = [sunny,cloudy_day,rain_day,night,cloudy_night,rain_night]
resized_images = list()
for img in images:
    new_img = img.resize((100,100))
    resized_images.append(new_img)

# Defining Resized Images
sunny_final = ImageTk.PhotoImage(resized_images[0])
cloudy_day_final = ImageTk.PhotoImage(resized_images[1])
rain_day_final = ImageTk.PhotoImage(resized_images[2])
night_final = ImageTk.PhotoImage(resized_images[3])
cloudy_night_final = ImageTk.PhotoImage(resized_images[4])
rain_night_final = ImageTk.PhotoImage(resized_images[5])

# Accessing the API
api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/karachi?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
api = json.loads(api_req.content) 

# Frame for Weather Icon and Temperature
frame1 = LabelFrame(root,borderwidth=0)
frame1.grid(row = 0,column=0,padx=(2,10))

# Weather Icon based on Conditions
time_init = time.time()
condition = api['days'][0]['conditions']
if time_init > api['days'][0]['sunriseEpoch'] and time_init < api['days'][0]['sunsetEpoch']:
    if 'CLEAR' in condition.upper():
        img_label = Label(frame1,image=sunny_final)
    elif 'RAIN' in condition.upper():
        img_label = Label(frame1,image=rain_day_final)
    elif 'CLOUDY' in condition.upper():
        img_label = Label(frame1,image=cloudy_day_final)
else:
    if 'CLEAR' in condition.upper():
        img_label = Label(frame1,image=night_final)
    elif 'RAIN' in condition.upper():
        img_label = Label(frame1,image=rain_night_final)
    elif 'CLOUDY' in condition.upper():
        img_label = Label(frame1,image=cloudy_night_final)

img_label.grid(row=0,column=0,rowspan=2)

# Current Temperature and Feels Like Temperature
current_temp_f = api['days'][0]['temp']
feelslike_temp_f = api['days'][0]['feelslike']

current_temp_c = round(5/9 *(current_temp_f-32))
feelslike_temp_c = round(5/9 *(feelslike_temp_f-32),1)

current_temp_label = Label(frame1,text = str(current_temp_c)+"°",font=("bebas neue",67,"bold"))
current_temp_label.grid(row=0,column=1)
degree_sign = Label(frame1,text="C",font=("bebas neue",32,"bold"),fg="gray")
degree_sign.grid(row=0,column=2,sticky=W)

feelslike_temp_label = Label(frame1,text = "RealFeel: "+str(feelslike_temp_c)+"°C",font=("bebas neue",16))
feelslike_temp_label.grid(row=1,column=1,sticky=N)

# Weather Condition
desc = api['days'][0]['conditions']
desc_label = Label(frame1,text = desc,font=("bebas kei",14,"bold"))
desc_label.grid(row=2,column=0,sticky=W,padx=10)

# More Details
more = Button(frame1,text="More Details >",font=("bebas kei",12,"bold"),borderwidth=0)
more.grid(row=3,column=0,sticky=W,padx=10)

# Frame for Important Details
frame2 = LabelFrame(root,borderwidth=0)
frame2.grid(row = 0,column=1,padx=10)

# Today's Time
time_label = Label(frame2,text = "Time: ",font = ("bebas neue",13))
time_label.grid(row=0,column=0,sticky=W)

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
        
        time_label2 = Label(frame2,text = str(new_time),font = ("bebas neue",12,"bold"))
        time_label2.grid(row=0,column=1,sticky=E)
        
        time.sleep(1)

# Time Offset
time_off = api['tzoffset']

# Creating Different Thread for Time
time_thread = threading.Thread(target=time_update, args=(time_off,))
time_thread.daemon = True
time_thread.start()

for i in range(1,6,2):
    locals()['trash_label'+str(i)] = Label(frame2,text = "_______________________________________________",fg="gray", font=("Arial", 8))
    locals()['trash_label'+str(i)].grid(row=i,column=0,columnspan=2)

# Today's Date
time_day = api['days'][0]['datetime']
time_day_label = Label(frame2,text = "Date: ",font = ("bebas neue",13))
time_day_label2 = Label(frame2,text = time_day,font = ("bebas neue",12,"bold"))

time_day_label.grid(row=2,column=0,sticky=W)
time_day_label2.grid(row=2,column=1,sticky=E)

# Getting Location from the Data
location = api['resolvedAddress']
location_label = Label(frame2,text = "Location: ",font = ("bebas neue",13))
location_label2 = Label(frame2,text = location,font=("bebas neue",12,"bold"))

location_label.grid(row=4,column=0,sticky=W)
location_label2.grid(row=4,column=1,sticky=E)

# Air Quality
air_quality = api['stations']['OPKC']['quality']
air_quality_label1 = Label(frame2,text = "Air Quality: ",font = ("bebas neue",13))
air_quality_label2 = Label(frame2,text = air_quality,font =("bebas neue",12,"bold"))

air_quality_label1.grid(row=6,column=0,sticky=W)
air_quality_label2.grid(row=6,column=1,sticky=E)

root.mainloop()