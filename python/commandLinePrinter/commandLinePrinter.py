from pprint import pprint as p
import sys
import time


arrayOfStringsToPrint = []

for progressCount in range(0, 8):

	time.sleep(0.1)
	newStringToPrint = 'progress: {}'.format(progressCount)
	
	for indexOfStringToPrint in range(len(arrayOfStringsToPrint)):
		sys.stdout.write("\x1b[1A\x1b[2K") # move up cursor and delete whole line

	arrayOfStringsToPrint.append(newStringToPrint)
	
	if len(arrayOfStringsToPrint) > 3:
		arrayOfStringsToPrint.pop(0)

	for indexOfStringToPrint in range(len(arrayOfStringsToPrint)):
		sys.stdout.write(arrayOfStringsToPrint[indexOfStringToPrint] + "\n") # reprint the lines


