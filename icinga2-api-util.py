#!/usr/bin/env python
# Description: Runs external API calls to the Icinga serer
# Requirements:
#	icinga2api libary (See Pipfile)
# See also: https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/#example-api-client-in-python

import argparse
import getpass
import json
import logging
import os
import requests
import sys

from icinga2api.client import Client

#
# logging
#

def initialize_logger():
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	 
	# create console handler and set level to WARN
	handler = logging.StreamHandler()
	if args.debug:
		formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	else:
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	 # create info file handler and set level to info
	handler = logging.FileHandler(log_filename + ".log", "w", encoding=None, delay="true")
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# create debug file handler and set level to debug
	handler = logging.FileHandler(log_filename + "-debug.log","w")
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

#
# Args
#

# Set the help_position/width values appropriatly to space our long argument text
# Avoid setting metavar/dest overrides to control argument output if don't you rely on it's value
aparser = argparse.ArgumentParser(description="Icinga API util for external requests",
formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog,max_help_position=60,width=90))
aparser.add_argument('-c', '--creds', help="Supply credentials file.")
aparser.add_argument('--check-result', action='store_true', help="Check result for action.")
aparser.add_argument('-dbg', '--debug', action='store_true', default=False, help="Debug output")
aparser.add_argument('-cert', '--cert', action='store', required=True, \
	help="Path to icinga.pem SSL cert (See /etc/pki/tls/certs ons server).")
aparser.add_argument('-f', '--filter', action='store', help="Filter API call with this string.")
aparser.add_argument('--host', action='store', help="Host object to target")
aparser.add_argument('--service', action='store', help="Service to target")
aparser.add_argument('-ln', '--log-name', action='store', default="icinga2-api-util", help="log filename")
aparser.add_argument('-t', '--test', action='store_true', help="Test functionality (ideally should be a unit test...)")
args = aparser.parse_args()

# Set logger
log_filename = os.environ['HOME'] + os.sep + args.log_name
initialize_logger()

# vars
if args.filter:
	filter = args.filter
else:
	filter = ''

# Authentication
if args.creds == None:
	username = raw_input("Icinga API username: ")
	password = getpass.getpass("Password: ")
else:
	# use supplied credentials file
	credentials_file = open(args.creds)
	line = credentials_file.readlines()
	username = line[0].rstrip()
	password = line[1].rstrip()
	credentials_file.close()

#
# Pre-checks
#

if args.cert:
	logging.info("Using SSL Cert")

if args.check_result and not (args.host and args.service):
	aparser.error("Host and service requried")

#
# vars
#

# Replace 'localhost' with your FQDN and certificate CN
# for SSL verification
# Note: URL here obtained via inspect tool on Overview > Services page
icinga_host = 'udaicinga.geisinger.edu'
icinga_port = '5665'
icinga_uri = "https://" + icinga_host + ":" + icinga_port
icinga_cert = args.cert

logging.info("Connecting to " + icinga_uri)
try:
	client = Client(icinga_uri, username, password,
		ca_certificate=icinga_cert)
except:
	raise
else:
	logging.info("Connection established")

# TESTING
if args.check_result:
	types = ['CheckResult']
	queue = 'monitor'
	filter = 'event.check_result.exit_status==2'

	for event in client.events.subscribe(types, queue, filter):
		print(event)

elif args.test:
	logging.info("\n\n====== host test ======")
	host = 'gdchdpmn01drlx.geisinger.edu'
	service = 'check-ping4'
	try:
		logging.info(client.objects.get('Host', host))
		logging.info("\n\n====== service " + service + " ======")
		logging.info(client.objects.get('Service', host + '!' + service))
		logging.info("\n\n====== test: service " + service + " (with attribs) ======")
		logging.info(client.objects.get('Service', host + '!' + service, joins=True))
		logging.info("\n\n====== test: host object list " + host + "======")
		logging.info(client.objects.list('Host'))
		logging.info("\n\n====== test: services with associated host " + host + "======")
		logging.info(client.objects.list('Service', joins=['host.name']))
		print "\n"
	except:
		raise

logging.info("Log: " + log_filename)

