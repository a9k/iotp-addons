#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Grab just items due today and print them out
# Written by Alan McNeil <a9k@a9k.info>
# MIT license.
from __future__ import print_function
import rtm_const
import sys
import webbrowser
from rtmapi import Rtm
from Adafruit_Thermal import *

if __name__ == '__main__':
    api = Rtm(rtm_const.api_key, rtm_const.shared_secret, "read", rtm_const.token)

    # authenication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
    # check for valid token
    if not api.token_valid():
        # use desktop-type authentication
        url, frob = api.authenticate_desktop()
        # open webbrowser, wait until user authorized application
        print ("URL you need to open: %s" % url)
        webbrowser.open(url)
        raw_input("Continue?")
        # get the token for the frob
        api.retrieve_token(frob)
        # print out new token, should be used to initialize the Rtm object next time
        print ("token: %s" % api.token)
        f1=open('./rtm_const', 'w+')
        f1.write("token: %s\n" % api.token)
        print ("You're going to need to remove the duplicate token line\n")
        f1.close

    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

    # get all open tasks, see http://www.rememberthemilk.com/services/api/methods/rtm.tasks.getList.rtm
    result = api.rtm.tasks.getList(filter="due:today")

    box     = chr(0xaf) # Degree symbol on thermal printer
    printer.println("------------------------------")
    for tasklist in result.tasks:
        for taskseries in tasklist:
            printer.print("{} {}\n".format(box, taskseries.name))

    printer.println("------------------------------")
