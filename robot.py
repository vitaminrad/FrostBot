import re
import PyCmdMessenger
import math
import time

arduino = PyCmdMessenger.ArduinoBoard('COM3', baud_rate=115200)

commands = [['motors','ff'],
			['energize',''],
			['deenergize',''],
			['motor_value_1','f'],
			['motor_value_2','f'],
			['energized','s']]

# Initialize the messenger
robot = PyCmdMessenger.CmdMessenger(arduino, commands)

# step config
ms_mode = 32
stepper_deg = 1.8
steps_per_rev = (360 * 32) / stepper_deg
steps_per_degree = ms_mode / stepper_deg

segment_distance = 1

# link lengths
la = 58
lb = 100
lc = 60

# default angles
curr_a1 = 90
curr_a4 = 90

dest_a1 = 0
dest_a4 = 0

curr_x = 0
curr_y = 0

dest_x = 0
dest_y = 0


def get_angles(x, y):
	E1 = float(-2 * la * x)
	F1 = float(-2 * la * y)
	G1 = float(la * la - lb * lb + x * x + y * y)

	E4 = float(2 * la * (-x + lc))
	F4 = float(-2 * la * y)
	G4 = float(lc * lc + la * la - lb * lb + x * x + y * y - (2 * lc * x))

	try:
		a1 = 2 * math.atan((-F1 + math.sqrt(E1 * E1 + F1 * F1 - G1 * G1)) / (G1 - E1))
	except:
		print('Coordinates are out of bounds.')
	try:
		a4 = 2 * math.atan((-F4 - math.sqrt(E4 * E4 + F4 * F4 - G4 * G4)) / (G4 - E4))
	except:
		print('Coordinates are out of bounds.')

	return (math.degrees(a1), math.degrees(a4))


def get_coords(a1, a4):
	a1 = math.radians(a1)
	a4 = math.radians(a4)

	A = 2 * lb * (lc + la * ( math.cos(a4) - math.cos(a1) ))
	B = 2 * la * lb * (math.sin(a4) - math.sin(a1))
	C = math.pow(lc, 2) + 2 * (la * la) + 2 * lc * la * math.cos(a4) - 2 * lc * la * math.cos(a1) - 2 * (la * la) * math.cos(a4 - a1)

	D = 2 * math.atan((-B - math.sqrt((A * A) + (B * B) - (C * C))) / (C - A))

	x = round(lc + la * math.cos(a4) + lb * math.cos(D))
	y = round(la * math.sin(a4) + lb * math.sin(D))

	return (x, y)


def get_segment_coords(dest_x, dest_y):
	D = math.sqrt((curr_x - dest_x) * (curr_x - dest_x) + (curr_y - dest_y) * (curr_y - dest_y))
	proposed_x = curr_x - ((segment_distance * (curr_x - dest_x)) / D)
	proposed_y = curr_y - ((segment_distance * (curr_y - dest_y)) / D)

	return (proposed_x, proposed_y)


def make_move(dest_x, dest_y):
	global curr_x, curr_y, curr_a1, curr_a4, moving

	(dest_a1, dest_a4) = get_angles(dest_x, dest_y)

	if dest_a1 > curr_a1:
		delta_a1 = dest_a1 - curr_a1
	else:
		delta_a1 = -abs(dest_a1 - curr_a1)

	if dest_a4 > curr_a4:
		delta_a4 = dest_a4 - curr_a4
	else:
		delta_a4 = -abs(dest_a4 - curr_a4)

	steps_motor_1 = (delta_a1 * steps_per_degree)
	steps_motor_2 = (delta_a4 * steps_per_degree)

	robot.send('motors', steps_motor_1, steps_motor_2)
	msg1 = robot.receive()
	msg2 = robot.receive()

	print(msg1)
	print(msg2)

	curr_a1 = dest_a1
	curr_a4 = dest_a4

	curr_x = dest_x
	curr_y = dest_y

	return


def main():
	global curr_x, curr_y, curr_a1, curr_a4

	# we know our initial angles so lets get coordinates...
	(curr_x, curr_y) = get_coords(curr_a1, curr_a4)

	robot.send('energize')
	msg = bool(robot.receive())

	with open('test.gcode') as gcode:
		for line in gcode:
			line = line.strip()
			coord_x = re.findall(r'X\d+.\d+', line)
			coord_y = re.findall(r'Y\d+.\d+', line)
			
			if coord_x and coord_y:
				dest_x = float(coord_x[0][1:])
				dest_y = float(coord_y[0][1:])

				dist = math.sqrt((curr_x - dest_x) * (curr_x - dest_x) + (curr_y - dest_y) * (curr_y - dest_y))

				if dist > segment_distance:
					while dist >= segment_distance:

						(proposed_x, proposed_y) = get_segment_coords(dest_x, dest_y)

						make_move(proposed_x, proposed_y)

						curr_x = proposed_x
						curr_y = proposed_y

						dist = math.sqrt((curr_x - dest_x) * (curr_x - dest_x) + (curr_y - dest_y) * (curr_y - dest_y))
				else:
					make_move(dest_x, dest_y)

	robot.send('deenergize')
	msg = bool(robot.receive())

if __name__ == '__main__':
	main()
