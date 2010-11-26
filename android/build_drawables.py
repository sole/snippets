import os
import tempfile
import Image
import argparse

# A script for building drawables from SVG inputs
# by sole / http://soledadpenades.com

def main(argv=None):

	# List of SVG files (without extension) we want to convert to drawables in different resolutions
	images = ['icon']
	
	cwd = os.getcwd()
	input_dir = os.path.join(cwd, '..', 'graphics')
	output_dir = os.path.join(cwd, '..', '..', 'res')

	parser = argparse.ArgumentParser(description='Build different resource asset versions')
	parser.add_argument('--images', help='Comma separated list of images to be converted', default='')
	parser.add_argument('--input-dir', dest='input_dir', help='Directory containing input SVG files', default=input_dir)
	parser.add_argument('--output-dir', dest='output_dir', help='Project res directory', default=output_dir)

	args = parser.parse_args()

	input_dir = args.input_dir
	output_dir = args.output_dir
	if len(args.images) > 0:
		images = args.images.split(',')

	output_versions = [
			{'name': 'drawable-ldpi', 'width': 36, 'height': 36},
			{'name': 'drawable-mdpi', 'width': 48, 'height': 48},
			{'name': 'drawable-hdpi', 'width': 72, 'height': 72},
		]

	for image in images:
		input_file = os.path.abspath(os.path.join(input_dir, image + '.svg'))
		
		print "\nProcessing", input_file

		if not os.path.exists(input_file):
			print "%s doesn't exist, skipped" % input_file
			continue

		# First export to bitmap with Inkscape
		temp_tuple = tempfile.mkstemp()
		temp_file = temp_tuple[1]
		inkscape_str = 'inkscape %s --export-png=%s --export-area-drawing' % (input_file, temp_file)
		os.system(inkscape_str)
		bitmap = Image.open(temp_file)

		# Then build resized versions
		for version in output_versions:
			output_file = os.path.abspath(os.path.join(output_dir, version['name'], image + '.png'))

			resized = bitmap.resize((version['width'], version['height']), Image.ANTIALIAS)
			resized.save(output_file, 'PNG')
		
		# clean up after ourselves :)
		os.unlink(temp_file)

if __name__ == '__main__':
	main()
