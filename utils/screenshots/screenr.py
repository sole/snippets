#!/usr/bin/python
"""

A simple program for taking periodical screenshots of your desktop
Usage is screenr.py [interval in secods]

E.g. screenr.py 30 will take a screenshot every 30 seconds

If no arguments are provided, interval is 5 seconds

Screenshots are saved with a screenshotYYYYMMDD_HHMMSS.png format

ImageMagick must be installed for this to work.

"""
import os
import time
import sys

if len(sys.argv) > 1:
	interval = float(sys.argv[1])
	if interval < 1:
		interval = 1
else:
	interval = 5

print "Capturing with ", interval, "seconds interval"

while True:
	print "cheese"

	str = "import -window root screenshot" + time.strftime("%Y%m%d_%H%M%S") + ".png"
	os.system(str)
	time.sleep(interval)
