import argparse
import telnetlib
import time
from datetime import datetime
from xml.dom.minidom import parseString

# Author sole http://soledadpenades.com

def parse_args():

	parser = argparse.ArgumentParser(description='Reproduce and simulate a GPS track.')

	parser.add_argument('--file', help='File containing the KML track', required=True) 

	parser.add_argument('--port', type=int, help='Telnet port where the emulator is listening to', default=5554)

	parser.add_argument('--interval', type=float, help='Interval between commands, in seconds', default=1)

	parser.add_argument('--realtime', help='Tries to replay using real time intervals (from metadata in each Placemark). If enabled, takes precedence over the interval value', action='store_const', const=True, default=False)

	parser.add_argument('--swap', help='Swap latitude and longitude values.', action='store_const', const=True, default=False)
	
	return parser.parse_args()


def run(args):
	with open(args.file, 'r') as f:
		kml_data = f.read()

	xml = parseString(kml_data)
	tn = telnetlib.Telnet('localhost', args.port)
	i = 1
	d0 = None
	interval = 0
	realtime = args.realtime

	placemarks = xml.getElementsByTagName('Placemark')
	print("Got %d place marks" % len(placemarks))
		
	for placemark in placemarks:

		coordinates = placemark.getElementsByTagName('coordinates')
		if coordinates is None:
			continue
					
		triad = coordinates[0].childNodes[0].nodeValue.split(',')
		if args.swap:
			triad[0], triad[1] = triad[1], triad[0]
		geo_cmd = ('geo fix ' + (' '.join(triad))).encode('latin-1')

		if realtime:	
			description = placemark.getElementsByTagName('description')

			if description is None:
				continue

			description = description[0].childNodes[0].nodeValue
			fix_type, timestamp, accuracy = description.split(':')
			d = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
		
			if d0 is not None:
				diff = d - d0
				interval = (diff.microseconds + (diff.seconds + diff.days * 24 * 3600) * 10**6) / 10**6 
				print 'difference', diff, interval

			d0 = d

		else:
			if i > 1:
				interval = args.interval
	
		time.sleep(interval)

		print i, geo_cmd
		tn.write(geo_cmd + "\r\n")

		i = i + 1

	tn.close()


def main(argv=None):
	args = parse_args()
	run(args)
	

if __name__ == "__main__":
	main()

