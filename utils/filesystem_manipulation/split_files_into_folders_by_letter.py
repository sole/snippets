# soledad penades www.soledadpenades.com

import os
import shutil
import sys

if len(sys.argv) > 1:
	folder = sys.argv[1]
else:
	folder = '.'

for item in os.listdir(folder):

	full_path = os.path.join(folder, item)
	
	if os.path.isdir(full_path):
		continue
	
	dst_folder = os.path.join(folder, item[0].lower())
	
	if not os.path.exists(dst_folder):
		os.mkdir(dst_folder)
		
	shutil.move(full_path, os.path.join(dst_folder, item))
