# FrostBot
5 Bar Parallel Robot controlled via Python and Arudino using CmdMessenger.  Inverse / forward kinematics are calculated in Python and steps are sent to Arduino via CmdMessenger.

## Python
`robot.py` will home and run circle.gcode

`energize.py` allows for stepper driver calibration (simply energizes motors)

`deenergize.py` de energize stepper motors

`generate_circle_gcode.py` generates simple gcode to draw a circle

## Arduino
`robot/robot.ino` is responsible for controlling the motors and performing the homing commands.
