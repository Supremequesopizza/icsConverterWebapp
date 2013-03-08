import logging
#import os
#
#import cgi
#import urllib
#import wsgiref.handlers
#
#from google.appengine.ext.webapp import template
#from google.appengine.ext import db
#from google.appengine.api import users
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app

#import csv
from icalendar import Calendar, Event, LocalTimezone
from datetime import datetime, timedelta
from random import randint
#import easygui
from sys import exit
from os.path import expanduser,isdir

#try:
#	if isdir(expanduser("~/Desktop")):
#	    reader = csv.reader(open(easygui.fileopenbox(msg="Please select the .csv file to be converted to .ics", title="", default=expanduser("~/Desktop/"), filetypes=["*.csv"]), 'rb'))
#	else:
#		reader = csv.reader(open(easygui.fileopenbox(msg="Please select the .csv file to be converted to .ics", title="", default=expanduser("~/"), filetypes=["*.csv"]), 'rb'))
#except:
#    exit(0)
#
#try:
##	print "got here"
#except:
#	pass

def convert(reader):


    #Start calendar file

#    Debug: worked fine here.
#    counter = 0
#    for row in reader:
#      counter += 1
#      logging.info("Here is row %s of reader: %s", counter, row)

    cal = Calendar()
    cal.add('prodid', 'n8henrie.com')
    cal.add('version', '2.0')
    
    #Run through the CSV row by row, processing its elements to cal
    rownum = 0;
    for row in reader:
        if rownum > 0 and row[0] != '':
          event = Event()
          event.add('summary', row[0])
    
    #If marked as an "all day event," ignore times. icalendar module doesn't like bare dates 
    #without times, so will default to midnight. Therefore add 1 day to end date to make a 24 
    #hour period. Set as transparent (= free / not busy). If start and end date are the same 
    #or if end date is blank default to a single 24-hour event.
          if row[5].lower() == "true":
            event.add('transp', "TRANSPARENT")
            event.add('dtstart', datetime.strptime(row[1], "%m/%d/%Y" ))
            if row[1] == row[3] or row[3] == '':
              event.add('dtend', datetime.strptime(row[1], "%m/%d/%Y" ) + timedelta(days=1))
            else:
              event.add('dtend', datetime.strptime(row[3], "%m/%d/%Y" ) + timedelta(days=1))
    
    #Continue processing events not marked as "all day event."
          else:
            if row[2][-2:].lower() in ['am','pm']:
              event.add('dtstart', datetime.strptime(row[1] + row[2], "%m/%d/%Y%I:%M %p" ))
            else:
              event.add('dtstart', datetime.strptime(row[1] + row[2], "%m/%d/%Y%H:%M" ))
    
    #Allow either 24 hour time or 12 hour + am/pm
            if row[4][-2:].lower() in ['am','pm']:
              event.add('dtend', datetime.strptime(row[3] + row[4], "%m/%d/%Y%I:%M %p" ))
            else:
              event.add('dtend', datetime.strptime(row[3] + row[4], "%m/%d/%Y%H:%M" ))
    
          event.add('description', row[6])
          event.add('location', row[7])
          event.add('dtstamp', datetime.replace( datetime.now(), tzinfo=LocalTimezone() ))
          event['uid'] = str(randint(1,10**30)) + datetime.now().strftime("%Y%m%dT%H%M%S") + '___n8henrie.com'
    
          cal.add_component(event)
        rownum += 1

#	easygui.msgbox("Looks like there was a problem parsing the .csv file.")
#    print "Error in processing the file. Please verify the format is exactly as specified."
    finalFile = cal.to_ical()

#    Logging commentary: Seemed to work fine here
#    logging.info("This is cal at line 93: %s", something)

    return finalFile
#  return cal.to_ical()

    #Write final .ics file to same directory as input file.
#try:
#    if isdir(expanduser("~/Desktop")):
#	    f = open(easygui.filesavebox(msg="Save .ics File", title="", default=expanduser("~/Desktop/") + "calendar.ics", filetypes=["*.ics"]), 'wb')
#    else:
#	    f = open(easygui.filesavebox(msg="Save .ics File", title="", default=expanduser("~/") + "calendar.ics", filetypes=["*.ics"]), 'wb')
#
#    f.write(cal.to_ical())
#    f.close()
#except:
#    pass