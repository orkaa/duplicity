# This script is to be used with Zabbix monitoring. It writes "backup.log", each time it runs, which can be parsed with Zabbix. If everything is correct, log will contain this string: "Status: GOOD"

import subprocess
import datetime
import sys

##### CONFIG #####
# How many days can pass between backups
DELTA = 1
##################

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

try:
	process = subprocess.Popen('./backup.sh status', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	output = process[0].split('\n')
	stderr = process[1]
	if stderr != "":
		print stderr
		sys.exit(1)	
except Exception, e:
	raise e
	
while True:
	if len(output) < 1:
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
	print("No recent backups. Last good: %s" % backup_time)
elif (current_time - backup_time) <= delta:
	logfile = file('backup.log', 'w')
	logfile.write('Last successful backup: %s\n' % backup_time)
	logfile.close()
	print('Last successful backup: %s' % backup_time)
else:
	print("No recent backups. Last good: %s" % backup_time)
