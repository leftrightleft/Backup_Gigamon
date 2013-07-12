#!/usr/bin/env python

import pexpect
import fileinput
import time
import argparse

#assign arguments
parser = argparse.ArgumentParser(description='This script runs the backup operation for Gigamons.  It requires a file called gmnlist.txt\nto be in the directory from which it\'s run.')
parser.add_argument('-u', help='SCP Username')
parser.add_argument('-s', help='SCP Server')
parser.add_argument('-p', help='SCP Password')
args = parser.parse_args()
arg_username = args.u
arg_password = args.p

#assign variables to aruguments
scp_server = args.s
scp_username = args.u
scp_password = args.p

#main function to backup config file of 2404s
def run_2404():
  try:
		child = pexpect.spawn ('ssh %s' % line) 
		child.expect ('password:')
		child.sendline ('%s\r\n' % scp_password)
		child.expect ('\w+>')
		child.sendline ('upload -cfg %s.cfg scp:%s@%s\r\n' % (line, scp_username, scp_server) ) 
		child.expect ('password:')
		child.sendline ('%s\r\n' % scp_password)
		child.expect ('\w+>')
		child.sendline ('quit')
		print line, 'successful'
	except:
		print line, 'failed'

#main functionto backup config file for H series
def run_h():
	try:
		child = pexpect.spawn ('ssh %s' % line) 
		child.expect ('Password:')
		child.sendline ('%s\r\n' % scp_password)
		child.expect ('\w+ >')
		child.sendline ('en\r\n')
		child.expect ('\w+ #')
		child.sendline ('config t\r\n')
		child.expect ('\w+ #')
		child.sendline ('config upload active scp://%s:%s@%s/home/%s/%s.cfg\r\n' % (scp_username, scp_password, scp_server, scp_username, line) ) 
		child.expect ('\w+ #')
		child.sendline ('quit')
		print line, 'successful'
	except:
		print line, 'failed'

#read the file gmnlist.txt		
for line in fileinput.input(['gmnlist.txt']):
	line = line.rstrip('\n')
	if not "H" in line:
		run_2404()
	else:
		run_h()
