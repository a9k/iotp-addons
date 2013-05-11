Addons for Python-Thermal-Printer
=================================
##just_forecast.py
Prints the weather summary by zipcode.
Each time you run
	./just_forecast.py
It will print city, sunrise, sunset, current conditions, and the forecast for today and tomorrow.
You'll need to set the ZIPCODE constant.

##fortune.py
Prints a fortune from the unix fortune collection.
Grabs unix fortunes until one is short enough to print. Rejustifies Q&A fortunes to fit better.

###Requirements
Install the fortune package at the command line on your device:
	sudo apt-get install fortune

Each time you run
	./fortune.py
you will get a fortune printed on the printer and displayed on the console.

##rtm_today.py
Prints any todos at your Remember the Milk account that are due today.

###Requirements
You'll need to get https://pypi.python.org/pypi/RtmAPI
It interface with Remember the Milk but it is in an "python egg". 
Copy the __init__.py into a file "rtmapi.py" and save that file in your Python-Thermal-Printer folder.
Getting setup with the RTM API is a bit of work. You'll need to get your won api key.
http://www.rememberthemilk.com/services/api/
And once you have the key back by email, you'll have to insert it into this script.
Even then it will FAIL because the first time you run it, you have to be in the web interface of RTM to approve access to your lists. The script will return a token that needs to be placed in the script (token).
I'm sorry I didn't take notes while I was trying this. I might have had to run the script on a desktop without printer first to get the token set.

