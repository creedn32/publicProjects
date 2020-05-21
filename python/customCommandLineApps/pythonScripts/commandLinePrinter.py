import sys
import time
from pprint import pprint as p


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





# import sys
# import time
# from collections import deque

# queue = deque([], 3)
# for t in range(20):
#     time.sleep(0.5)
#     s = "update %d" % t
#     for _ in range(len(queue)):
#         sys.stdout.write("\x1b[1A\x1b[2K") # move up cursor and delete whole line
#     queue.append(s)
#     for i in range(len(queue)):
#         sys.stdout.write(queue[i] + "\n") # reprint the lines





#####################################################################################################


# for printCount in range(0, 5):
# 	print(printCount)
# 	time.sleep(.5)
	
# 	if printCount != 4:
# 		sys.stdout.write("\033[F") # Cursor up one line
# 		# sys.stdout.write("\x1b[1A\x1b[2K") # move up cursor and delete whole line




#####################################################################################################


# import time

# for x in range (0, 5):  
#	 b = "Loading" + "." * x
#	 print(b, end="\r")
#	 time.sleep(1)


#####################################################################################################

# import sys
# import time

# for i in range(10):
#	 print("Loading" + "." * i)
#	 sys.stdout.write("\033[F") # Cursor up one line
#	 time.sleep(.1)


#####################################################################################################

# CURSOR_UP_ONE = '\x1b[1A' 
# ERASE_LINE = '\x1b[2K'

# print('first line')
# print('second line')

# data_on_first_line = CURSOR_UP_ONE + CURSOR_UP_ONE + ERASE_LINE + "abc"
# sys.stdout.write(data_on_first_line)

# data_on_second_line = "def\r"
# sys.stdout.write(data_on_second_line)
# sys.stdout.flush()


#####################################################################################################

# import curses
# import time

# def report_progress(filename, progress):
#	 """progress: 0-10"""
#	 stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
#	 stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))
#	 stdscr.refresh()

# if __name__ == "__main__":
#	 stdscr = curses.initscr()
#	 curses.noecho()
#	 curses.cbreak()

#	 try:
#		 for i in range(10):
#			 report_progress("file_{0}.txt".format(i), i+1)
#			 time.sleep(0.5)
#	 finally:
#		 curses.echo()
#		 curses.nocbreak()
#		 curses.endwin()


#####################################################################################################

# from reprint import output
# import time

# if __name__ == "__main__":
#	 with output(output_type='dict') as output_lines:
#		 for i in range(10):
#			 output_lines['Moving file'] = "File_{}".format(i)
#			 for progress in range(100):
#				 output_lines['Total Progress'] = "[{done}{padding}] {percent}%".format(
#					 done = "#" * int(progress/10),
#					 padding = " " * (10 - int(progress/10)),
#					 percent = progress
#					 )
#				 time.sleep(0.05)
