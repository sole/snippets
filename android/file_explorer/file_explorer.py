import os, subprocess, argparse, time

"""

file_explorer --device_list /mnt/sdcard/
file_explorer --copy_from_device /mnt/sdcard/pdf --copy_to_host .
file_explorer --copy_from_computer ./local_files --copy_to_device /mnt/sdcard/device_files

"""


def parse_args():

	parser = argparse.ArgumentParser(description='Read/write files from/to Android devices via ADB')

	parser.add_argument('--adb', help="Location of adb binary", default='adb')
	parser.add_argument('--device_list', help="List device files", default=False)
	parser.add_argument('--copy_from_device', help='Copy a file (or directory) from the device', default=False)
	parser.add_argument('--copy_to_host', help='When used with --copy_from_device, specifies where to copy files', default='.')
	parser.add_argument('--copy_from_host', help='Copy a file (or directory) from the host to the device', default=False)
	parser.add_argument('--copy_to_device', help='When used with --copy_from_host, specifies where to copy files', default='.')

	return parser.parse_args()

def execute(command):
	print "EXECUTE=", command
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout

	lines = []

	while True:
		line = process.readline()
		
		if not line:
			break

		lines.append(line)
	
	return lines


def device_list(adb, device_dir):

	command = "%s shell ls -l %s" % (adb, device_dir)
	lines = execute(command)
	return lines


def parse_device_list(lines):

	entries = {}

	for line in lines:
		line = line.rstrip()

		parts = line.split(None, 6)

		if len(parts) == 6:
			# Directories don't report their size
			permissions, owner, group, mdate, mtime, filename = parts
			fsize = 0

		elif len(parts) == 7:
			permissions, owner, group, fsize, mdate, mtime, filename = parts

		is_directory = permissions.startswith('d')
		timestamp = time.mktime((time.strptime(mdate + ' ' + mtime, "%Y-%m-%d %H:%M")))

		entries[filename] = { 'is_directory': is_directory, 'size': fsize, 'timestamp': timestamp }



	return entries

def is_device_file_a_directory(adb, device_file):
	parent_dir = os.path.dirname(device_file)
	filename = os.path.basename(device_file)
	lines = device_list(adb, parent_dir)
	entries = parse_device_list(lines)

	if not entries.has_key(filename):
		return False

	return entries[filename]['is_directory']


# Exposed actions

def action_device_list(adb, device_dir):
	lines = device_list(adb, device_dir)
	for line in lines:
		print line.rstrip()

def action_copy_from_device(adb, device_file, host_directory):
	print "COPY FROM DEVICE: ", device_file, "=>", host_directory

	if os.path.isfile(host_directory):
		print "ERROR", host_directory, "is a file, not a directory"
		return

	if is_device_file_a_directory(adb, device_file):
		print device_file, "is a dir"

		# copy recursively!
		entries = parse_device_list(device_list(adb, device_file))

		for filename, entry in entries.iteritems():
			if entry['is_directory']:
				action_copy_from_device(adb, os.path.join(device_file, filename), os.path.join(host_directory, filename))
			else:
				print "Should copy", filename
				action_copy_from_device(adb, os.path.join(device_file, filename), host_directory)

	else:
		print device_file, "is a file"

		host_file = os.path.join(host_directory, os.path.basename(device_file))
		print "copying to", host_file
		command = '%s pull "%s" "%s"' % (adb, device_file, host_file)
		execute(command)

def action_copy_from_host(adb, host_file, device_directory):
	print "-------"
	print "COPY FROM HOST:", host_file, "=>", device_directory

	fixed_device_dir = os.path.normpath(device_directory)
	print "FIXED =>", fixed_device_dir
	dst_parent_dir = os.path.dirname(fixed_device_dir)
	# Can't use os.path.basename as it doesn't return the name part of a directory
	# (it comes out as an empty string!)
	(dst_path, dst_basename) = os.path.split(fixed_device_dir)
	parent_device_entries = parse_device_list(device_list(adb, dst_parent_dir))

	print "PARENT", dst_parent_dir
	print "BASENAME", dst_basename
	print "CONTAINS", parent_device_entries


	if not parent_device_entries.has_key(dst_basename):
		print "hop", dst_basename, dst_parent_dir
		command = '%s shell mkdir "%s" ' % (adb, device_directory )
		execute(command)

	elif not parent_device_entries[dst_basename]['is_directory']:
		print "ERROR", device_directory, "is a file, not a directory"
		return

	if os.path.isfile(host_file):
		print host_file, "is a file"

		entries = parse_device_list(device_list(adb, device_directory))
		f = os.path.basename(host_file)
		if entries.has_key(f):
			if entries[f]['timestamp'] >= os.path.getmtime(host_file) and entries[f]['size'] == os.path.getsize(host_file):
				print "File is newer or the same, skipping"
				return

		print "Copying", host_file, "=>", device_directory

		command = '%s push "%s" "%s"' % (adb, host_file, device_directory)
		execute(command)
	else:
		print host_file, 'is a directory'

		entries = os.listdir(host_file)

		for entry in entries:
			action_copy_from_host(adb, os.path.join(host_file, entry), os.path.join(device_directory, os.path.basename(host_file)))

# ~~~

def run(args):

	if args.device_list:
		action_device_list(args.adb, args.device_list)
	
	elif args.copy_from_device:
		action_copy_from_device(args.adb, args.copy_from_device, args.copy_to_host)
	
	elif args.copy_from_host:
		action_copy_from_host(args.adb, args.copy_from_host, args.copy_to_device)



	
def main(argv=None):
	args = parse_args()
	run(args)

if __name__ == "__main__":
	main()

