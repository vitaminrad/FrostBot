import os
import sys
import csv
import getopt
import math


def main(argv):

	output_filename = 'circle.gcode'
	x0 = 25
	y0 = 100
	points = 48
	radius = 34

	try:
		opts, args = getopt.getopt(argv, "ho:p:r:x:y:", ["output_file=", "points=", "radius=", 'x=', 'y='])
	except getopt.GetoptError:
		print('generate_circle_gcode.py -o <output_file>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('generate_circle_gcode.py -o <output_file> -r <radius> -x <x> -y <y>')
			sys.exit()
		elif opt in ("-o", "--output_file"):
			output_filename = arg
		elif opt in ("-p", "--points"):
			points = int(arg)
			print('Setting points: %d' % points)
		elif opt in ("-r", "--radius"):
			radius = float(arg)
			print('Setting radius: %f' % radius)
		elif opt in ("-x", "--x"):
			x0 = float(arg)
			print('Setting x: %f' % x0)
		elif opt in ("-y", "--y"):
			y0 = float(arg)
			print('Setting y: %f' % y0)


	with open(output_filename, 'w') as output_file:

		for i in range(points):
			x = x0 + radius * math.cos(2 * math.pi * i / points)
			y = y0 + radius * math.sin(2 * math.pi * i / points)

			g_line = 'G1 X%f Y%f' % (x, y)

			print(g_line)

			output_file.write(g_line + "\n")

	print('Created: %s' % output_filename)

if __name__ == "__main__":
	main(sys.argv[1:])