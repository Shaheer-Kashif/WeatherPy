import requests, json, datetime, time
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from urllib.request import urlopen

first = 1

# Main Tkinter Window
root = Tk()
root.title("WeatherPy")
root.iconbitmap("icons/weatherimage.ico")
    
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

# Getting Location
url='http://ipinfo.io/json'
response=urlopen(url)

# Extracting it in a Readable Format
current_location = json.load(response)
city = current_location['city']
country = current_location['country']

# Accessing the API
api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+city+"%20"+country+"?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
api = json.loads(api_req.content) 

# Getting the Location based on Entry
def get_location():
    global api_req,api,search,root
    pass_var = False
    if search.get() == "":
        pass
    else:
        temp = search.get()
        temp = temp.lower()
        if " " in search.get():
            temp = temp.replace(" ","%20")
        try:
            api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+temp+"?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
            api = json.loads(api_req.content)
            pass_var = True
        except:
            messagebox.showerror("Error","Invalid Input or Place")
        if pass_var == True:
            refresh_info()

# Time Update Func after Every Second
def time_update():
    global frame2,root,time_label2,time_off
    # Loop for Updating Time
            
    # Getting Current Time in Epoch Format
    time_epoch = time.time()
            
    # Converting to Readable Format
    real_time = datetime.datetime.utcfromtimestamp(time_epoch)
            
    # Checking the Time Zone Offset is in Decimal or not and setting the time according to that
    if time_off == int(time_off):
        time_to_add = datetime.timedelta(hours=time_off, minutes=0, seconds=0)
    else:
        decimal_part = time_off % 1
        time_to_add = datetime.timedelta(hours=int(time_off), minutes=decimal_part*60, seconds=0)
            
    # Adding the Offset and GMT Time to get Final Time
    new_time = real_time + time_to_add
            
    # Adding the Offset and GMT Time to get Final Time
    new_time = new_time.strftime('%H:%M:%S')
    time_label2.config(text = str(new_time))

    # 1 second delay to update time again
    time_label2.after(1000, time_update)
        
def display_more():
    # Disabling buttons to avoid conflict of windows and location
    global more,search_button
    more.config(state=DISABLED)
    search_button.config(state=DISABLED)
    
    # Creating new window
    new_window = Toplevel()
    
    # Weather Description
    # Create Frame
    desc_frame = LabelFrame(new_window,borderwidth=0)
    desc_frame.grid(row = 0,column=0,columnspan=2)
    
    # Getting Description from API
    description = api['days'][0]['description']
    
    # Creating Description Labels
    desc_label = Label(desc_frame,text = "Description: ",font = ("bebas neue",13))
    desc_label2 = Label(desc_frame,text = description,font = ("bebas neue",12,"bold"))
    
    # Placing Description Labels
    desc_label.grid(row=0,column=0,sticky=W)
    desc_label2.grid(row=0,column=1,sticky=E)
    
    frame1_n = LabelFrame(new_window,borderwidth=0)
    frame1_n.grid(row=1,column=0,padx=(2,10))
    
    frame2_n = LabelFrame(new_window,borderwidth=0)
    frame2_n.grid(row=1,column=1,padx=(2,10))
    
    uv_index = api['days'][0]['uvindex']
    str_uv = str(int(uv_index))
    if uv_index >= 0 and uv_index <= 2:
        uv_index = str_uv + " (Low)"
    elif uv_index >= 3 and uv_index <= 5:
        uv_index = str_uv + " (Moderate)"
    elif uv_index >= 6 and uv_index <= 7:
        uv_index = str_uv + " (High)"
    elif uv_index >= 8 and uv_index <= 10:
        uv_index = str_uv + " (Very High)"
        
    uv_index_label = Label(frame1_n,text = "UV Index: ",font = ("bebas neue",13))
    uv_index_label2 = Label(frame1_n,text = uv_index,font = ("bebas neue",12,"bold"))
    uv_index_label.grid(row=0,column=0,sticky=W)
    uv_index_label2.grid(row=0,column=1,sticky=E)
    
    visibility = api['days'][0]['visibility']
    visibility_label = Label(frame1_n,text = "Visibility: ",font = ("bebas neue",13))
    visibility_label2 = Label(frame1_n,text = str(visibility) + " km",font = ("bebas neue",12,"bold"))
    visibility_label.grid(row=1,column=0,sticky=W)
    visibility_label2.grid(row=1,column=1,sticky=E)
    
    
    humidity = api['days'][0]['humidity']
    str_hum = str(int(humidity))
    if humidity < 30:
        humidity = str_hum +"% (Dry)"
    elif humidity >= 30 and humidity <= 60:
        humidity = str_hum +"% (Moderate)"
    elif humidity >= 60 and humidity <= 80:
        humidity = str_hum +"% (High)"
    elif humidity > 80:
        humidity = str_hum +"% (Very High)"
        
    humidity_label = Label(frame1_n,text = "Humidity: ",font = ("bebas neue",13))
    humidity_label2 = Label(frame1_n,text = humidity,font = ("bebas neue",12,"bold"))
    
    humidity_label.grid(row=2,column=0,sticky=W)
    humidity_label2.grid(row=2,column=1,sticky=E)

    precip = int(api['days'][0]['precipprob'])
    precip_label = Label(frame1_n,text = "Precipitation Probability: ",font = ("bebas neue",13))
    precip_label2 = Label(frame1_n,text = str(precip)+"%",font = ("bebas neue",12,"bold"))
    precip_label.grid(row=3,column=0,sticky=W)
    precip_label2.grid(row=3,column=1,sticky=E)
    
    

    
    sunrise = api['days'][0]['sunrise']
    
    sunrise_label = Label(frame2_n,text = "Sunrise: ",font = ("bebas neue",13))
    sunrise_label2 = Label(frame2_n,text = sunrise ,font = ("bebas neue",12,"bold"))
    
    sunrise_label.grid(row=0,column=0,sticky=W)
    sunrise_label2.grid(row=0,column=1,sticky=E)
    
    sunset = api['days'][0]['sunset']
    
    sunset_label = Label(frame2_n,text = "Sunset: ",font = ("bebas neue",13))
    sunset_label2 = Label(frame2_n,text = sunset ,font = ("bebas neue",12,"bold"))
    
    sunset_label.grid(row=1,column=0,sticky=W)
    sunset_label2.grid(row=1,column=1,sticky=E)
    
    min_temp_f = api['days'][0]['tempmin']
    min_temp_c = round(5/9 *(min_temp_f-32))
    
    min_temp_label = Label(frame2_n,text = "Min Temperature: ",font = ("bebas neue",13))
    min_temp_label2 = Label(frame2_n,text = str(min_temp_c)+"°C" ,font = ("bebas neue",12,"bold"))
    
    min_temp_label.grid(row=2,column=0,sticky=W)
    min_temp_label2.grid(row=2,column=1,sticky=E)
    
    max_temp_f = api['days'][0]['tempmax']
    max_temp_c = round(5/9 *(max_temp_f-32))
    
    max_temp_label = Label(frame2_n,text = "Max Temperature: ",font = ("bebas neue",13))
    max_temp_label2 = Label(frame2_n,text = str(max_temp_c)+"°C" ,font = ("bebas neue",12,"bold"))
    
    max_temp_label.grid(row=3,column=0,sticky=W)
    max_temp_label2.grid(row=3,column=1,sticky=E)
    
    
def refresh_info():
    global search,first,root,frame2,root,time_label2,time_off,more,search_button
    
    # Main Tkinter Window, If Program is executed 1st then it reads the images from the outside
    # otherwise from the inside because of a bug
    if first == 1:
        first = 0
        global sunny_final,cloudy_day_final,rain_day_final,night_final,cloudy_night_final,rain_night_final
    else:
        root.destroy()
        root = Tk()
        root.title("WeatherPy")
        root.iconbitmap("icons/weatherimage.ico")
        
        sunny_final = ImageTk.PhotoImage(resized_images[0])
        cloudy_day_final = ImageTk.PhotoImage(resized_images[1])
        rain_day_final = ImageTk.PhotoImage(resized_images[2])
        night_final = ImageTk.PhotoImage(resized_images[3])
        cloudy_night_final = ImageTk.PhotoImage(resized_images[4])
        rain_night_final = ImageTk.PhotoImage(resized_images[5])
            
    # Dark Mode or Light Mode, depending on time.
    time_init = time.time()
    if time_init > api['days'][0]['sunriseEpoch'] and time_init < api['days'][0]['sunsetEpoch']:
        root.configure(bg = "white")
        root.option_add('*background', 'white')
        root.option_add('*foreground', 'black')
    else:
        root.configure(bg = "#2b2b2b")
        root.option_add('*background', '#2b2b2b')
        root.option_add('*foreground', 'white')
        
    # Frame 1
    frame1 = LabelFrame(root,borderwidth=0)
    frame1.grid(row=1,column=0,padx=(2,10))
        
    # Frame 2
    frame2 = LabelFrame(root,borderwidth=0)
    frame2.grid(row = 1,column=1,padx=10)

    # Frame for Searching Location
    entry_frame = LabelFrame(root,borderwidth=0)
    entry_frame.grid(row=3,column=0,columnspan=2,pady=10)

    search = Entry(entry_frame,bg="white",fg="black",font=("Helvetica",14))
    search.pack()

    search_button = Button(entry_frame,text="Search Location",font = ("bebas kei",14,"bold"),command=get_location,bg="#0086D3",fg="white",width = 18)
    search_button.pack(pady=(5,0))

    # Frame 1 Work
    
    # Weather Icon based on Conditions
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
    more = Button(frame1,text="More Details >",font=("bebas kei",12,"bold"),borderwidth=0,command = display_more)
    more.grid(row=3,column=0,sticky=W,padx=10)

    # Frame 2 Work
    # Today's Time
    time_label = Label(frame2,text = "Time: ",font = ("bebas neue",13))
    time_label.grid(row=0,column=0,sticky=W)

    # Time Offset
    time_off = api['tzoffset']

    # Creating Different Thread for Time
    time_label2 = Label(frame2,text = "00:00:00",font = ("bebas neue",12,"bold"))
    time_label2.grid(row=0,column=1,sticky=E)
    
    time_update()
    
    # Today's Date
    try:
        time_day = api['days'][0]['datetime']
    except KeyError:
        time_day = "Error"
    time_day_label = Label(frame2,text = "Date: ",font = ("bebas neue",13))
    time_day_label2 = Label(frame2,text = time_day,font = ("bebas neue",12,"bold"))

    time_day_label.grid(row=2,column=0,sticky=W)
    time_day_label2.grid(row=2,column=1,sticky=E)

    # Getting Location from the Data
    try:
        location = api['resolvedAddress']
    except KeyError:
        location = "Error"
    location_label = Label(frame2,text = "Location: ",font = ("bebas neue",13))
    location_label2 = Label(frame2,text = location,font=("bebas neue",12,"bold"))

    location_label.grid(row=4,column=0,sticky=W)
    location_label2.grid(row=4,column=1,sticky=E)

    # Air Quality
    try:
        wind_speed = api['days'][0]['windspeed']
    except KeyError:
        wind_speed = "Error"
    wind_speed_label1 = Label(frame2,text = "Wind Speed: ",font = ("bebas neue",13))
    wind_speed_label2 = Label(frame2,text = str(wind_speed)+" km/hr",font =("bebas neue",12,"bold"))

    wind_speed_label1.grid(row=6,column=0,sticky=W)
    wind_speed_label2.grid(row=6,column=1,sticky=E)
    
    for i in range(1,6,2):
        line = "_" *len(location)
        locals()['trash_label'+str(i)] = Label(frame2,text = line + "________________________________",fg="gray", font=("Arial", 8))
        locals()['trash_label'+str(i)].grid(row=i,column=0,columnspan=2,sticky=W+E)
        
    root.mainloop()

refresh_info()
