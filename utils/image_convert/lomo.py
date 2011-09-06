import argparse
import os
import shutil


""" "Lomify" pictures

	Grossly incomplete and unfinished.
	
	Based on these, and other misc ImageMagick tricks out there
		http://the.taoofmac.com/space/blog/2005/08/23/2359
		https://github.com/soveran/lomo
"""


def parse_args():
	parser = argparse.ArgumentParser(description='Lomify pictures')
	parser.add_argument('--in', help='Input files', dest='in_files', metavar='image1 [image2 image3... imageN]', nargs='*', required=True)
	parser.add_argument('--width', help='Output width', type=int, required=False, default=1024)
	parser.add_argument('--height', help='Output height', type=int, required=False, default=768)
	parser.add_argument('--use-mask', help='Use feather mask', dest='use_mask', default=True, action='store_true')
	parser.add_argument('--black-and-white', help='Convert to grayscale', dest='black_and_white', default=False, action='store_true')
	parser.add_argument('--use-grain', help='Add grain', dest='use_grain', default=False, action='store_true')
	
	args = parser.parse_args()

	return args

def execute(cmd):
	print "EXEC: " + cmd
	os.system(cmd)

def process(args):

	lomo_mask = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lomo_mask.png'))

	"""if args.use_mask:
		lomo_mask = os.path.abspath(os.path.join(os.path.dirname(args.in_files[0]), 'tmp_lomo_mask.png'))
		execute("convert -size %dx%d xc: -fx '(1-(2*i/w-1)^4)*(1-(2*j/h-1)^4)' %s" % (args.width / 10, args.height / 10, lomo_mask))
		execute("mogrify -resize %dx%d -gaussian 0x5 %s" % (args.width, args.height, lomo_mask))"""
	
	for src_file in args.in_files:
		
		base_dir, filename = os.path.split(src_file)
		base_file, extension = os.path.splitext(filename)
		print extension
		if extension.lower().endswith('.jpg'):
			format = 'jpg'
		else:
			format = 'png'
		
		dst_file = os.path.join(base_dir, base_file + '_lomo' + extension)
		dst_file_resized = dst_file + '_resized'
		
		commands = [
			'cp %s %s' % (src_file, dst_file),
			'convert -resize %dx%d %s %s' % (args.width, args.height, dst_file, dst_file),
			'cp %s %s' % (dst_file, dst_file_resized),
			#'convert -unsharp 1 -contrast -contrast  -modulate 100,150 %s %s' % (dst_file, dst_file),
			'convert -contrast -contrast %s %s' % (dst_file, dst_file),
			'convert -modulate 100,150 %s %s' % (dst_file, dst_file),
		]
		
		"""if args.use_grain:
			commands.append('composite ( +clone +level-colors GREY50 -attenuate 6 +noise Poisson -colorspace Gray ) -compose Overlay -composite %s %s' % (dst_file, dst_file))"""
		
		if args.use_mask:
			commands.append('composite -compose overlay %s %s %s' % (lomo_mask, dst_file, dst_file))
		
		commands.append('composite -compose multiply %s %s %s' % (dst_file_resized, dst_file, dst_file))

		if args.black_and_white:
			commands.append('mogrify -type Grayscale %s' % dst_file)
		
		commands.append('rm %s' % (dst_file_resized))


		[execute(cmd) for cmd in commands]

	"""if args.use_mask:
		execute('rm %s' % lomo_mask)"""

def main(argv=None):
	args = parse_args()
	process(args)


if __name__ == "__main__":
	main()
