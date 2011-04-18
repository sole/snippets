import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description='Gently make sure your NetGear router has still a valid DHCP lease from Be broadband')
parser.add_argument('--router-address', dest='router_address', help="Your router's control address", default='http://192.168.0.1')
parser.add_argument('--ping-address', dest='ping_address', help="Which external URL we'll use to 'ping' the 'outside world'", default='http://www.google.com')
parser.add_argument('--user', help="Your router's admin username", default='admin')
parser.add_argument('--password', help="Admin's password", default='admin')

input_arguments = parser.parse_args()

ROUTER_ADDRESS = input_arguments.router_address
PING_ADDRESS = input_arguments.ping_address
USER = input_arguments.user
PASS = input_arguments.password

# --- do not edit below ---

STATUS_PAGE = ROUTER_ADDRESS + '/st_dhcp.htm'
SETUP_PAGE = ROUTER_ADDRESS + '/setup.cgi'

BASE_CMD = 'curl --user %s:%s ' % (USER, PASS)
BASE_ARGS = [ 'curl', '--user', '%s:%s' % (USER,PASS) ]

def run_args(args):
	print "*"*20
	print 'Running', ' '.join(args)
	p = subprocess.Popen(args, stdout=subprocess.PIPE)
	out = p.communicate()[0]
	print "."*20
	return out

# Check there is a network connection before
conn_ok = run_args(['curl', PING_ADDRESS])
if conn_ok.find("Couldn't resolve host") != -1:

	# First request is just for authorising the session
	run_args(BASE_ARGS + [ROUTER_ADDRESS]) 

	# Request release
	release_out = run_args(BASE_ARGS + ['--data', 'release=Release&todo=release', SETUP_PAGE])

	# Request renewal
	renewal_out = run_args(BASE_ARGS + ['--data', 'connect=Renew&todo=renew', SETUP_PAGE])
	print renewal_out

	lease_obtained = False
	status_args = BASE_ARGS + [STATUS_PAGE]
	num_attempts = 0

	while num_attempts < 10 and lease_obtained == False:
		
		print "Waiting 10 secs before checking again"
		time.sleep(10)

		status_out = run_args(status_args)
		print status_out

		if(status_out.find("<TD NOWRAP>---</td>") == -1):
			print "Yay! lease renewed!"
			lease_obtained = True

		num_attempts = num_attempts + 1

else:
	print "Connection is working"


