#!/usr/bin/python

"""

Convert all wav files in the current directory to ogg files, 
using oggenc

To get oggenc in ubuntu: apt-get vorbis-tools

Based on this snippet: http://snippets.dzone.com/posts/show/5868

"""

import os, re

cwd = os.getcwd()

audio_files = [file for file in os.listdir(cwd) if re.search(r'.wav$', file)]

for filename in audio_files:
	ogg_filename = re.sub(r'.wav$', '.ogg', filename)
	cmd = "oggenc -o " + ogg_filename + " " + filename
	print 'running', cmd
	os.system(cmd)
	
