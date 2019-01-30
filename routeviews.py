#!/usr/bin/python3
# routeviews.py
# import the library
import pexpect
import argparse
from sys import exit

# Argument configurations
try:
	ArgParse = argparse.ArgumentParser()
	ArgParse.add_argument('-r', '--bgpv4route', type=str, required=True, help="Check ipv4 route in routing table")
	ARGS = ArgParse.parse_args()

except:
	print("Argument Function Failed!")
	exit(1)

if __name__ == "__main__":
        pass
else:
        exit(1)

# Start Program
try:
	if ARGS.bgpv4route is not None:
		routeviews = pexpect.spawn('telnet route-views.routeviews.org')
		routeviews.expect('Username:')
		routeviews.sendline('rviews')
		routeviews.expect('route-views>')
		routeviews.sendline("show bgp ipv4 unicast {} bestpath".format(ARGS.bgpv4route))
		routeviews.expect('route-views>')

		print(routeviews.before.decode('ascii'))

		routeviews.sendline('exit')

except:
	print("Main Program Failed!")
	exit(1)
