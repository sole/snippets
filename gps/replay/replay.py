import argparse
import telnetlib
import time
from xml.dom.minidom import parseString

# Author sole http://soledadpenades.com

def parse_args():

	parser = argparse.ArgumentParser(description='Reproduce and simulate a GPS track.')

	parser.add_argument('--file', help='File containing the KML track', required=True) 

	parser.add_argument('--port', type=int, help='Telnet port where the emulator is listening to', default=5554)

	parser.add_argument('--interval', type=float, help='Interval between commands, in seconds', default=1)

	parser.add_argument('--swap', help='Swap latitude and longitude values.', action='store_const', const=True, default=False)
	
	return parser.parse_args()


def run(args):
	with open(args.file, 'r') as f:
		kml_data = f.read()

	xml = parseString(kml_data)

	coordinate_nodes = xml.getElementsByTagName('coordinates')

	print("Got %d coordinates" % len(coordinate_nodes))

	tn = telnetlib.Telnet('localhost', args.port)

	i = 1
	for coord in coordinate_nodes:
		triad = coord.childNodes[0].nodeValue.split(',')
		if args.swap:
			tmp_arg = triad[0]
			triad[0] = triad[1]
			triad[1] = tmp_arg
		geo_cmd = ('geo fix ' + (' '.join(triad))).encode('latin-1')
		print i, geo_cmd

		tn.write(geo_cmd + "\r\n")
		time.sleep(args.interval)

		i = i + 1
	
	tn.close()


def main(argv=None):
	args = parse_args()
	run(args)
	

if __name__ == "__main__":
	main()

