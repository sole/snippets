# soledad penades www.soledadpenades.com

import os
import shutil
import sys
import time
from datetime import datetime

if len(sys.argv) > 1:
	folder = sys.argv[1]
else:
	folder = '.'

for item in os.listdir(folder):

	full_path = os.path.join(folder, item)
	
	if os.path.isdir(full_path):
		continue
	
        try:
            ctime = os.path.getctime(full_path)
        except OSError:
            ctime = 0

        try:
            mtime = os.path.getmtime(full_path)
        except OSError:
            mtime = 0

        final_time = min(ctime, mtime)

        created_date = time.ctime(ctime)
        modified_date = time.ctime(mtime)
        fu = time.ctime(final_time)
        d = datetime.strptime(fu,"%a %b %d %H:%M:%S %Y")
        final_date = d.strftime('%Y%m%d')
        
        print (created_date, modified_date, final_date)
        subfolder = final_date

	dst_folder = os.path.join(folder, subfolder)
	
	if not os.path.exists(dst_folder):
		os.mkdir(dst_folder)
	
        new_path = os.path.join(dst_folder, item)
        print (full_path, "=>", new_path)
        
	shutil.move(full_path, os.path.join(dst_folder, item))
