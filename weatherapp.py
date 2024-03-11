import requests, json, datetime, time
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from urllib.request import urlopen

first = 1
new_window = None
display_pass = True

# Getting Location
url='http://ipinfo.io/json'
try:
    response=urlopen(url)
    current_location = json.load(response)
    
    # Extracting it in a Readable Format
    city = current_location['city']
    country = current_location['country']
    
except:
    messagebox.showerror("Error","Could not Get Location due to No Internet Connection")
    quit()
    
# Accessing the API
api_req = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+city+"%20"+country+"?unitGroup=us&include=days&key=MBRFCLLUGNCW5BFQ2GVSJ99HG&contentType=json")
api = json.loads(api_req.content) 

# Main Tkinter Window
root = Tk()
root.title("WeatherPy")
root.iconbitmap("icons/weatherimage.ico")
    
# Defining Weather Icon Images (Large Size)
sunny_final = ImageTk.PhotoImage(Image.open("icons/sun.png"))
cloudy_day_final = ImageTk.PhotoImage(Image.open("icons/cloudy.png"))
rain_day_final = ImageTk.PhotoImage(Image.open("icons/rain.png"))
night_final = ImageTk.PhotoImage(Image.open("icons/night.png"))
cloudy_night_final = ImageTk.PhotoImage(Image.open("icons/cloudy-night.png"))
rain_night_final = ImageTk.PhotoImage(Image.open("icons/rainy-night.png"))

# Defining Weather Icon Images (Small Size)
sunny_small = ImageTk.PhotoImage(Image.open("icons/sun-small.png"))
cloudy_day_small = ImageTk.PhotoImage(Image.open("icons/cloudy-small.png"))
rain_day_small = ImageTk.PhotoImage(Image.open("icons/rain-small.png"))
drop_small = ImageTk.PhotoImage(Image.open("icons/drop.png"))

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
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error","No Internet Access Found")
        except:
            messagebox.showerror("Error","Invalid Input or Place")
        if pass_var == True:
            refresh_info()

# Time Update Function after Every Second
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

# Search Button Disable based on New Window
def search_button_disable():
    global search_button,new_window
    try:
        if new_window.winfo_exists():
            search_button.config(state=DISABLED)
        else:
            search_button.config(state=ACTIVE)
    except:
        pass
    search_button.after(500,search_button_disable)
    
# More Details Window Function
def display_more():
    # Disabling buttons to avoid conflict of windows and location
    global new_window,display_pass,sunny_small,rain_day_small,cloudy_day_small,drop_small,theme
    
    # Calling Search Button Disable Function
    search_button_disable()
    
    # First Time Creating and Destroying a Window so the window property is associated with the variable
    if display_pass == True:
        new_window = Toplevel()
        display_pass = False
        new_window.destroy()
       
    # Chcking if the window exists
    if new_window.winfo_exists():
        pass
    else:
        # Creating new window
        new_window = Toplevel()
        if theme == "day":
            new_window.configure(bg = "white")
            new_window.option_add('*background', 'white')
            new_window.option_add('*foreground', 'black')
        else:
            new_window.configure(bg = "#2b2b2b")
            new_window.option_add('*background', '#2b2b2b')
            new_window.option_add('*foreground', 'white')
        
        # More Info
        # Create Frame
        desc_frame = LabelFrame(new_window,borderwidth=0)
        desc_frame.grid(row = 0,column=0,columnspan=2)
        
        desc_label = Label(desc_frame,text = "More Details",font = ("bebas neue",12,"bold"))
        
        desc_label.grid(row=0,column=0,columnspan=2)
        
        # Creating 1st Details Frame
        frame1_n = LabelFrame(new_window,borderwidth=1)
        frame1_n.grid(row=1,column=0)
        
        # UV Value
        uv_index = api['days'][0]['uvindex']
        str_uv = str(int(uv_index))
        
        # Categorizing UV Value
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
        
        # Visiility in KMs
        visibility = api['days'][0]['visibility']
        
        visibility_label = Label(frame1_n,text = "Visibility: ",font = ("bebas neue",13))
        visibility_label2 = Label(frame1_n,text = str(visibility) + " km",font = ("bebas neue",12,"bold"))
        
        visibility_label.grid(row=1,column=0,sticky=W)
        visibility_label2.grid(row=1,column=1,sticky=E)
        
        # Humidity Value
        humidity = api['days'][0]['humidity']
        str_hum = str(int(humidity))
        
        # Categorizing Humidity Value
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

        # Precipitation Probability
        precip = int(api['days'][0]['precipprob'])
        
        precip_label = Label(frame1_n,text = "Rain/Snow Chances: ",font = ("bebas neue",13))
        precip_label2 = Label(frame1_n,text = str(precip)+"%",font = ("bebas neue",12,"bold"))
        
        precip_label.grid(row=3,column=0,sticky=W)
        precip_label2.grid(row=3,column=1,sticky=E)
        
        # Creating 2nd Details Frame
        frame2_n = LabelFrame(new_window,borderwidth=1)
        frame2_n.grid(row=1,column=1)
        
        # Sunrise Value
        sunrise = api['days'][0]['sunrise']
        
        sunrise_label = Label(frame2_n,text = "Sunrise: ",font = ("bebas neue",13))
        sunrise_label2 = Label(frame2_n,text = sunrise ,font = ("bebas neue",12,"bold"))
        
        sunrise_label.grid(row=0,column=0,sticky=W)
        sunrise_label2.grid(row=0,column=1,sticky=E)
        
        # Sunset Value
        sunset = api['days'][0]['sunset']
        
        sunset_label = Label(frame2_n,text = "Sunset: ",font = ("bebas neue",13))
        sunset_label2 = Label(frame2_n,text = sunset ,font = ("bebas neue",12,"bold"))
        
        sunset_label.grid(row=1,column=0,sticky=W)
        sunset_label2.grid(row=1,column=1,sticky=E)
        
        # Minimum Temperature Value
        min_temp_f = api['days'][0]['tempmin']
        min_temp_c = round(5/9 *(min_temp_f-32))
        
        min_temp_label = Label(frame2_n,text = "Min Temperature: ",font = ("bebas neue",13))
        min_temp_label2 = Label(frame2_n,text = str(min_temp_c)+"°C" ,font = ("bebas neue",12,"bold"))
        
        min_temp_label.grid(row=2,column=0,sticky=W)
        min_temp_label2.grid(row=2,column=1,sticky=E)
        
        # Maximum Temperature Value
        max_temp_f = api['days'][0]['tempmax']
        max_temp_c = round(5/9 *(max_temp_f-32))
        
        max_temp_label = Label(frame2_n,text = "Max Temperature: ",font = ("bebas neue",13))
        max_temp_label2 = Label(frame2_n,text = str(max_temp_c)+"°C" ,font = ("bebas neue",12,"bold"))
        
        max_temp_label.grid(row=3,column=0,sticky=W)
        max_temp_label2.grid(row=3,column=1,sticky=E)
        
        # Creating 3rd Details Frame (5 Days Extended Forecast)
        frame3_n = LabelFrame(new_window,borderwidth=0)
        frame3_n.grid(row=2,column=0,columnspan=2)
        
        weather_forecast = Label(frame3_n,text = "5 Day Weather Forecast",font = ("bebas neue",14),borderwidth=0)
        weather_forecast.grid(row=0,column=0)
        
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        current_date = datetime.datetime.now()
        curr_day = weekday_names[current_date.weekday()]


        for i in range(1,6):
            locals()["day"+str(i)] = LabelFrame(frame3_n,borderwidth=1)
            locals()["day"+str(i)].grid(row=i,column=0)
            
            locals()["labelday"+str(i)] = LabelFrame(locals()["day"+str(i)],borderwidth=0)
            locals()["labelday"+str(i)].grid(row=0,column=0)
            if i == 1:
                locals()["dayname"+str(i)] = Label(locals()["labelday"+str(i)],text=curr_day[0:3].upper(),font=("helvetica",10,"bold"))
            else:
                next_date = current_date + datetime.timedelta(days=i-1)
                locals()["dayname"+str(i)] = Label(locals()["labelday"+str(i)],text=weekday_names[next_date.weekday()][0:3].upper(),font=("helvetica",10,"bold"))
            locals()["dayname"+str(i)].grid(row=0,column=0)
            date = api['days'][i-1]['datetime']
            locals()["date"+str(i)] = Label(locals()["labelday"+str(i)],text=date[5:])
            locals()["date"+str(i)].grid(row=1,column=0)   

            locals()["weather"+str(i)] = LabelFrame(locals()["day"+str(i)],borderwidth=0)
            locals()["weather"+str(i)].grid(row=0,column = 1)
            
            locals()["condition"+str(i)] = api['days'][i-1]['conditions']
            
            if 'CLEAR' in locals()["condition"+str(i)].upper():
                img_label = Label(locals()["weather"+str(i)],image=sunny_small)
            elif 'RAIN' in locals()["condition"+str(i)].upper():
                img_label = Label(locals()["weather"+str(i)],image=rain_day_small)
            elif 'CLOUDY' in locals()["condition"+str(i)].upper():
                img_label = Label(locals()["weather"+str(i)],image=cloudy_day_small)
            img_label.grid(row=0,column=0)
            
            max_temp = api['days'][i-1]['tempmax']
            max_temp_cel = round(5/9 *(max_temp-32))
            
            min_temp = api['days'][i-1]['tempmin']
            min_temp_cel = round(5/9 *(min_temp-32))
            
            temp1 = Label(locals()["weather"+str(i)],text = str(max_temp_cel)+"°" ,font = ("bebas neue",12,"bold"))
            temp2 = Label(locals()["weather"+str(i)],text = str(min_temp_cel)+"°" ,font = ("bebas neue",10),fg="gray")
            
            temp1.grid(row=0,column=1)
            temp2.grid(row=0,column=2)
            
            # Weather Description
            description = api['days'][i-1]['description']
            
            locals()["desc"+str(i)] = Label(locals()["weather"+str(i)],text = description ,font = ("bebas neue",11))
            locals()["desc"+str(i)].grid(row=0,column=3)
            
            locals()["precip"+str(i)] = LabelFrame(locals()["day"+str(i)],borderwidth=0)
            locals()["precip"+str(i)].grid(row=0,column = 2)
            
            day_precip = int(api['days'][i-1]['precipprob'])
            precip_img_label = Label(locals()["precip"+str(i)],image=drop_small)
            precip_img_label.grid(row=0,column=0)
            
            precip_label1 = Label(locals()["precip"+str(i)],text = str(day_precip)+"%",font = ("bebas neue",11),fg="gray")
            precip_label1.grid(row=0,column=1)
            
            
            
            
            
def refresh_info():
    global search,first,root,frame2,root,time_label2,time_off,more,search_button,display_pass,theme
    
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
        
        display_pass = True

        sunny_final = ImageTk.PhotoImage(Image.open("icons/sun.png"))
        cloudy_day_final = ImageTk.PhotoImage(Image.open("icons/cloudy.png"))
        rain_day_final = ImageTk.PhotoImage(Image.open("icons/rain.png"))
        night_final = ImageTk.PhotoImage(Image.open("icons/night.png"))
        cloudy_night_final = ImageTk.PhotoImage(Image.open("icons/cloudy-night.png"))
        rain_night_final = ImageTk.PhotoImage(Image.open("icons/rainy-night.png"))
            
    # Dark Mode or Light Mode, depending on time.
    time_init = time.time()
    if time_init > api['days'][0]['sunriseEpoch'] and time_init < api['days'][0]['sunsetEpoch']:
        theme = "day"
        root.configure(bg = "white")
        root.option_add('*background', 'white')
        root.option_add('*foreground', 'black')
    else:
        theme = "night"
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
    current_temp_label.grid(row=0,column=1,sticky=E)
    degree_sign = Label(frame1,text="C",font=("bebas neue",32,"bold"),fg="gray")
    degree_sign.grid(row=0,column=2,sticky=W)

    feelslike_temp_label = Label(frame1,text = "RealFeel: "+str(feelslike_temp_c)+"°C",font=("bebas neue",16))
    feelslike_temp_label.grid(row=1,column=1,sticky=W)

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
    wind_speed = api['days'][0]['windspeed']
    
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
