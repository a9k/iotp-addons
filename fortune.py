#!/usr/bin/python
# Print out a reformatted unix fortune on a small thermal printer
# 
# Author: Alan McNeil <a9k@a9k.info>
# MIT license.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack
from __future__ import print_function
__author__ = 'Alan McNeil <a9k@a9k.info>'
__source__ = 'https://github.com/a9k'
import re
import sys
import textwrap
import subprocess,re
import textwrap
from Adafruit_Thermal import *

MAX_LINES_OF_FORTUNE = 6

# initialize the printer
printer     = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

# Get a fortune short enough to print
while 1:
    quip = subprocess.check_output("/usr/games/fortune") # get the output from the fortune command
    # remove formatting used on wide terminals like TAB
    reformatted_quip = re.sub('(\n\t|\t\t|\t|\n)',' ',quip).rstrip()
    lines = textwrap.wrap(reformatted_quip, 32) # wrap lines at 32 characters
    line_count = len(lines)     # how many lines is it?
    if (line_count<=MAX_LINES_OF_FORTUNE):  # if less than max lines
     break                      # we can use this fortune         

# print the lines
for line in lines:
  printer.print('{:<32}'.format(line))

printer.feed(max(4,6-line_count))    # eject the fortune by padding out to 6 lines min

# also put fortune on console output for verification and enjoyment.
print ('\n'.join(textwrap.wrap(reformatted_quip, 32)))
