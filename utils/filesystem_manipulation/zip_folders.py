# soledad penades www.soledadpenades.com

import os
import sys
import zipfile


if len(sys.argv) > 1:
	folder = sys.argv[1]
else:
	folder = '.'
        
for item in os.listdir(folder):
	
	full_path = os.path.join(folder, item)
	
	if not os.path.isdir(full_path):
		continue
	
	dst_filename = item + '.zip'
	
	dst_item = os.path.join(folder, dst_filename)
	
	
	if os.path.exists(dst_item) and os.path.getsize(dst_item) > 0:
		continue
	
	output_file = zipfile.ZipFile(dst_item, "w", zipfile.ZIP_DEFLATED)
	
	for item_file in os.listdir(full_path):
		output_file.write(os.path.join(full_path, item_file), item_file)
		
	output_file.close()
	
