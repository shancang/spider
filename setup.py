# -*- coding: utf-8
from  spider.common import *
import time
import os
import sys

def start():
	if os.path.isfile(PID_FILE):
		f=open(PID_FILE,'r')
		pid=f.read()
		print "Spider Is Running .... PID %s" % pid
		f.close()
		return 0
	os.system( "$(which python) spider/spider.py")
	time.sleep(2)
	if os.path.isfile(PID_FILE):
		f=open(PID_FILE,'r')
		
		pid=f.read()
		print "Spider Started .... PID %s" % pid
		return 0
	print "Spider Start Filed .... "

def stop():
	if os.path.isfile(PID_FILE):
		f=open(PID_FILE,'r')
		pid=f.read()
		os.system("kill -9 %s" % pid)
		os.remove(PID_FILE)
		print "Spider Stoped .... "
		return 0
	print "Spider Is Not Running  .... "
def status():
	if os.path.isfile(PID_FILE):
		f=open(PID_FILE,'r')
		pid=f.read()
		print "Spider Is Running .... PID %s" % pid
		return 0
	print "Spider Is Not Running  .... "

def helps():
	print "Usage: python %s start|stop|status" % sys.argv[0]

server={"start":start,"stop":stop,"status":status,"helps":helps}
if len(sys.argv) != 2 or sys.argv[1] not in server.keys():
	server["helps"]()
	sys.exit(1)
par=sys.argv[1]
server[par]()

