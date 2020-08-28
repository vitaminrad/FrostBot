import re
import PyCmdMessenger
import math
import time

arduino = PyCmdMessenger.ArduinoBoard('COM3', baud_rate=115200)

commands = [['motors', 'ff'],
			['energize', ''],
			['deenergize', ''],
			['home_axis', ''],
			['motor_value_1', 'f'],
			['motor_value_2', 'f'],
			['energized', 's'],
			['homed', 's']]

# Initialize the messenger
robot = PyCmdMessenger.CmdMessenger(arduino, commands)

def main():
	# kill motors...
	robot.send('deenergize')
	msg = robot.receive()

if __name__ == '__main__':
	main()
