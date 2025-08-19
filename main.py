
# WEATHER DISPLAY - Bartosz Jaskulski
#
#
# --- PLEASE READ ---
# This script is for Pimoroni Inky *wHAT* Displays ONLY
# Please use impression-main.py if you have an Inky Impression
# --- PLEASE READ ---
#add to 
# crontab -e
# /home/pi/.virtualenvs/pimoroni/bin/python /home/pi/weather-report/main.py


import os, sys
from datetime import datetime, timedelta
import cond_icons

import configparser

#config.ini file
configObj = configparser.ConfigParser()
configObj.read("/home/pi/weather-report/configfile.ini")
OWMAPI = configObj["OWM_API"]
UserLoc = configObj["Location"]

api = OWMAPI["api"]

lat =float(UserLoc["latitude"])
lon = float(UserLoc["longitude"])
city = str(UserLoc["city"])
country = str(UserLoc["country"])

#Inky Libraries
from inky import InkyWHAT
from PIL import Image, ImageFont, ImageDraw

# pyOWM Libraries
from pyowm.owm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

CURR_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
RESOURCES = CURR_DIR + "resources/"

# Fonts
PIXEL_FONT = RESOURCES + "fonts/Pixel12x10.ttf"
Terminal_FONT = RESOURCES + "fonts/terminal-grotesque.ttf"
Mister_Pixel_FONT = RESOURCES + "fonts/Mister_Pixel_Regular.otf"
B_FONT = RESOURCES + "fonts/04B_03.ttf"
VG5000_FONT = RESOURCES + "fonts/VG5000-Regular.otf"
FT88Reg_FONT = RESOURCES + "fonts/FT88-Regular.otf"

TimeDate = datetime.now()

degreeSign = u"\N{DEGREE SIGN}"

#OpenWeatherMap Integration
owm = OWM(api)
mgr = owm.weather_manager()
weather = mgr.weather_at_place(city+","+country).weather

getTemp = weather.temperature("fahrenheit") #enables temp in fahrenheit
curTemp = int(getTemp["temp"]) #get current temp

#Current "feels like" Temperature
feelsLike = int(getTemp["feels_like"])
currentFeelsLike = "Feels: "+str(feelsLike)+degreeSign

#current max and min temps
maxTemp = int(getTemp["temp_max"])
minTemp = int(getTemp["temp_min"])

#Current wind speeds
getWind = weather.wind(unit="miles_hour")
curWind = int(getWind["speed"])

inky_display = InkyWHAT("yellow")
inky_display.set_border(inky_display.WHITE)

Location_ICON = RESOURCES + "icons/location.png"
LocationIcon = Image.open(Location_ICON)

img = Image.open("/home/pi/weather-report/resources/background/weather-report-bg.png")
draw = ImageDraw.Draw(img)

font_tiny = ImageFont.truetype(FT88Reg_FONT, 12)
font_small = ImageFont.truetype(FT88Reg_FONT, 12)
font_medium = ImageFont.truetype(VG5000_FONT, 32)
font_medium2 = ImageFont.truetype(FT88Reg_FONT, 18)
font_big = ImageFont.truetype(VG5000_FONT, 70)
font2 = ImageFont.truetype(VG5000_FONT, 10)

currentTemp = str(curTemp)+degreeSign

currentMaxTemp = "Max: "+str(maxTemp)+degreeSign #current temp max
currentMinTemp = "Min: "+str(minTemp)+degreeSign #current temp min


currentCond = str(weather.status)
currentDetailCond = str(weather.detailed_status).title()

currentWind = "Wind:"+str(curWind)+" MPH"
currentLoc = ": " + city

#proper text placement
projectName = "WEATHER REPORT"
bbox = font2.getbbox(projectName)
w_name = bbox[2] - bbox[0]
h_name = bbox[3] - bbox[1]

x_name = 200 - (w_name/2)

#draw data and text onto display

draw.text((5, 4),TimeDate.strftime("%m-%d-%Y"), inky_display.WHITE, font2)     #Time
draw.text((350, 4),TimeDate.strftime("%I:%M %p"), inky_display.WHITE, font2)      #Date
draw.text((x_name, 4),projectName, inky_display.WHITE, font2)                  #project name

draw.text((155, 65), currentTemp, inky_display.BLACK, font_big)                #Current temp
draw.text((292, 100), currentMaxTemp, inky_display.BLACK, font_small)          #Current max temp
draw.text((292, 116), currentMinTemp, inky_display.BLACK, font_small)          #Current min temp
draw.text((292, 70), currentFeelsLike, inky_display.BLACK, font_small)

img.paste(LocationIcon, (15, 208))
draw.text((35, 210), currentLoc, inky_display.BLACK, font_medium2)             #Current location

draw.text((292, 178), currentWind, inky_display.BLACK, font_small)             #Current wind speed in MPH

draw.text((10, 190), currentDetailCond, inky_display.BLACK, font_medium2)      #Current weather conditions, detailed
img.paste(cond_icons.CurrCondIcon(), (15, 60))                                  #Current Weather Icon

inky_display.set_image(img)
inky_display.show()
