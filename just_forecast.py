#!/usr/bin/python

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from Yahoo! weather, prints current conditions and
# forecasts for next two days.  See timetemp.py for a different
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
#
# Rewritten by Alan McNeil <a9k@a9k.info> to add more information and take up less lines
#
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import urllib, time
import re
from Adafruit_Thermal import *
from xml.dom.minidom import parseString

# Use the zipcode interface
ZIPCODE = '59901'
deg     = chr(0xf8) # Degree symbol on thermal printer

# Convert degree to compass direction
def degToCompass8(num):
	"""Convert degrees into compass direction (8 points not pirates' 16)"""
	val=int((int(num)/45)+.5)
	yarr=["N","NE","E","SE", "S", "SW", "W", "NW"]
	return yarr[(val % 16)]

# Print out the city name
def city():
	tag     = 'yweather:location'
	city    = dom.getElementsByTagName(tag)[0].getAttribute('city')
	printer.inverseOn()
	printer.print('{:^32}\n'.format(city))
	printer.inverseOff()

# Print sunrise and sunset
def suntimes():
	tag     = 'yweather:astronomy'
	sunup   = dom.getElementsByTagName(tag)[0].getAttribute('sunrise')
	sundown = dom.getElementsByTagName(tag)[0].getAttribute('sunset')
	printer.print("Sunup {} - Sundown {}\n".format(sunup, sundown))

# Print out the current condition
def current_conditions():
	temp = dom.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
	cond = dom.getElementsByTagName('yweather:condition')[0].getAttribute('text')
	printer.print("{} {}{}".format(cond, temp,deg))

	wind_chill = dom.getElementsByTagName('yweather:wind')[0].getAttribute('chill')
	wind_dir = dom.getElementsByTagName('yweather:wind')[0].getAttribute('direction')
	wind_speed = dom.getElementsByTagName('yweather:wind')[0].getAttribute('speed')
	speed_unit = dom.getElementsByTagName('yweather:units')[0].getAttribute('speed')
	printer.print("({}) {} {}{}".format(wind_chill, degToCompass8(wind_dir), wind_speed, speed_unit))

	humidity = dom.getElementsByTagName('yweather:atmosphere')[0].getAttribute('humidity')
	visibility = dom.getElementsByTagName('yweather:atmosphere')[0].getAttribute('visibility')
	vis_unit = dom.getElementsByTagName('yweather:units')[0].getAttribute('distance')
	printer.print(" {}% {}{}\n".format(humidity, visibility,vis_unit))

# Dumps one forecast line to the printer
def forecast(idx):
    tag     = 'yweather:forecast'
    day     = dom.getElementsByTagName(tag)[idx].getAttribute('day')
    lo      = dom.getElementsByTagName(tag)[idx].getAttribute('low')
    hi      = dom.getElementsByTagName(tag)[idx].getAttribute('high')
    condition = dom.getElementsByTagName(tag)[idx].getAttribute('text')
    condition = re.sub('Thunderstorms','TStorms',condition) # make line too long
    printer.print("{}: {}{} - {}{} {}\n".format(day, lo, deg, hi,deg, condition))

# Initialize printer
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Fetch forecast data from Yahoo!, parse resulting XML
dom = parseString(urllib.urlopen(
        'http://weather.yahooapis.com/forecastrss?p=' + ZIPCODE).read())

city()		# Print city heading
suntimes()	# Print sunrise and sunset
current_conditions() # Print current conditions

# Print forecast for today and tomorrow
forecast(0)
forecast(1)
