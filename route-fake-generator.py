#!/usr/bin/python3
# route-fake-generator.py (NXOS)
# import the library
import ipaddress
import argparse
from sys import exit

# Argument configurations
try:
	ArgParse = argparse.ArgumentParser()
	ArgParse.add_argument('-r', '--route', type=str, required=True, help="Range IPv4 (ex: 10.0.0.0/8)")
	ArgParse.add_argument('-p', '--prefix', type=int, required=True, help="Prefix IPv4 (ex: 22)")
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
	file = open('./route.txt', 'w')
	for subnet in ipaddress.ip_network(ARGS.route).subnets(new_prefix=ARGS.prefix):
		file.write("ip route {0} Null0 name test\n".format(subnet))
	file.close()

except:
	print("Main Program Failed!")
	exit(1)
