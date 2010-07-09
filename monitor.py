# This script is to be used with Zabbix monitoring. It writes "backup.log", each time it runs, which can be parsed with Zabbix. If everything is correct, log will contain this string: "Status: GOOD"

import subprocess
import datetime
import sys

##### CONFIG #####
# How many days can pass between backups
DELTA = 2
##################

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

logfile = file('backup.log', 'w')

try:
	process = subprocess.Popen('./backup.sh status', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	output = process[0].split('\n')
	stderr = process[1]
	if stderr != "":
		logfile.write('Something wrong with the backup script:\n%s\nStatus: BAD\n' % stderr)
		logfile.close()
		print stderr
		sys.exit(1)	
except Exception, e:
	logfile.write('Something wrong with the backup script:\n%s\nStatus: BAD\n' % e)
	logfile.close()
	raise e
	
while True:
	if len(output) < 1:
		logfile.write('No backups so far.\n\nStatus: BAD\n')
		logfile.close()
		print "No backups so far."
		sys.exit(1)	
	line = output.pop().strip().split()
	if ("Incremental" or "Full") in line:
		clock = line[4].split(':')
		break

backup_time = datetime.datetime(int(line[5]), int(months[line[2]]), int(line[3]), int(clock[0]), int(clock[1]), int(clock[2]))

current_time = datetime.datetime.now()

delta = datetime.timedelta(int(DELTA))

if (current_time - backup_time) >= delta:
	logfile.write('Backup did not complete in given time.\nLast good: %s\nStatus: BAD\n' % backup_time)
	logfile.close()
	print "fail"
else:
	logfile.write('Backup successful.\nLast good: %s\nStatus: GOOD\n' % backup_time)	
	logfile.close()
	print "good"
