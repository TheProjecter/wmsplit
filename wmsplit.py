"""
	Wmsplit
	
	This program and documentation is free software; you can redistribute 
	it under the terms of the  GNU General Public License as published by
	the  Free Software Foundation;  either version 2  of the License,  or
	(at your option) any later version.
	
	This  program  is  distributed  in  the hope that it will be useful,
	but  WITHOUT ANY WARRANTY;  without  even  the  implied  warranty of
	MERCHANTABILITY  or  FITNESS  FOR  A  PARTICULAR  PURPOSE.  See  the
	GNU General Public License for more details.

	You  should  have  received a copy of the GNU General Public License
	along  with  this  program;  if  not,  write  to  the  Free Software
	Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
	
"""
 
# Import libs we need
import subprocess
import string
import sys

from optparse import OptionParser

# getoutput function
def getoutput (cmd):
	# Run the command
	try:
		output = subprocess.Popen(cmd,stdout=subprocess.PIPE)
	except OSError as error:
		traceback.print_exc(file=sys.stdout)
		return False
				
	# Return
	return output.communicate()[0]
	
# Parse command line options
parser = OptionParser(version="%prog 1.0")
parser.add_option(
	'-l', 
	'--left', 
	action = 'store_true',
	dest = 'left',
	help = 'place active window to the left side of you\'re screen',
	default = False
)

parser.add_option(
	'-r', 
	'--right', 
	action = 'store_true',
	dest = 'right',
	help = 'place active window to the right side of you\'re screen',
	default = False
)

parser.add_option(
	'-u', 
	'--up', 
	action = 'store_true',
	dest = 'up',
	help = 'maximize the active window',
	default = False
)

parser.add_option(
	'-d', 
	'--down', 
	action = 'store_true',
	dest = 'down',
	help = 'unmaximize the active window',
	default = False
)

parser.add_option(
	'--spacing-x', 
	type='int',
	dest = 'spacing_x',
	help = 'add spacing to the horizontal sides of the window',
	default = 0
)

parser.add_option(
	'--spacing-y', 
	type='int',
	dest = 'spacing_y',
	help = 'add spacing to the vertical sides of the window',
	default = 0
)

parser.add_option(
	'--no-vert-maximize', 
	action = 'store_true',
	dest = 'no_vert_maximize',
	help = 'do not maximize the window vertically',
	default = False
)
(options, args) = parser.parse_args()

# Maximize the window
if options.up == True:
	getoutput(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,maximized_vert,maximized_horz'])
	exit()

# Unmaximize the window
if options.down == True:
	getoutput(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,maximized_vert,maximized_horz'])
	exit()
	
if options.no_vert_maximize != True:
	getoutput(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,maximized_vert,maximized_horz'])
else:
	getoutput(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,maximized_vert'])
		
# Get screen dimensions
xdpy = subprocess.Popen(["xdpyinfo"], stdout=subprocess.PIPE)
grep = subprocess.Popen(['grep', 'dimensions:'], stdin=xdpy.stdout, stdout=subprocess.PIPE)
dimensions = grep.communicate()[0]
dimensions = dimensions.split('dimensions:', 2)
dimensions = dimensions[1].split('pixels')
dimensions = dimensions[0].strip()
dimensions = dimensions.split('x')

# Calculate the new dimensions
half_x	= int(int(dimensions[0]) / 2)
size_x 	= half_x - (options.spacing_x * 2)
size_y 	= int(dimensions[1]) - options.spacing_y

# Calculate the offset
offset_y = options.spacing_y

if options.left == True:
	offset_x = options.spacing_x
else:
	offset_x = half_x + options.spacing_x
	
# Resize the window and stuff :)
cmd = [
	'wmctrl', 
	'-r',
	':ACTIVE:',
	'-e',
	'0,' + str(offset_x) + ',' + str(offset_y) + ',' + str(size_x) + ',' + str(size_y)
]

print(getoutput(cmd))
