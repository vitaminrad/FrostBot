import math

# length of arms
L1 = 80.0 # both lower arms
L2 = 120.0 # left upper arm to pen
L3 = 12.0 # pen to left upper arm joint
L4 = 120.0 # right upper arm

# origin points of left and right servo
O1X = 0.0
O1Y = 0.0
O2X = 60.0
O2Y = 0.0

# double return_angle(double a, double b, double c) {
#   # cosine rule for angle between c and a
#   return acos((a * a + c * c - b * b) / (2 * a * c));
# }

def return_angle(a, b, c):
	return math.acos((a * a + c * c - b * b) / (2 * a * c))


# Tx, Ty = Target X,Y
def set_XY(Tx, Ty):

	dx = 0.0
	dy = 0.0
	c = 0.0
	a1 = 0.0
	a2 = 0.0
	Hx = 0.0
	Hy = 0.0

	# double dx, dy, c, a1, a2, Hx, Hy;

	# Calcutlating the left servo angle

	# calculate triangle between pen, servoLeft and arm joint
	# cartesian dx/dy
	dx = float(Tx) - O1X
	dy = float(Ty) - O1Y

	print (dx, dy, O1X, O1Y)

	# polar lemgth (c) and angle (a1)
	c = math.sqrt(dx * dx + dy * dy)
	a1 = math.atan2(dy, dx)
	a2 = return_angle(L1, L2, c)

	# servo2.writeMicroseconds(floor(((a2 + a1 - math.pi) * SERVOFAKTORLEFT) + SERVOLEFTNULL));

	thetaL = math.floor(a2 + a1 - math.pi)

	# Calcutlating the right servo angle

	# calculate joint arm point for triangle of the right servo arm (joint near the pen)
	a2 = return_angle(L2, L1, c)
	Hx = Tx + L3 * math.cos((a1 - a2 + 0.621) + math.pi)
	Hy = Ty + L3 * math.sin((a1 - a2 + 0.621) + math.pi)

	# calculate triangle between pen joint, servoRight and arm joint
	dx = Hx - O2X;
	dy = Hy - O2Y;

	c = math.sqrt(dx * dx + dy * dy)
	a1 = math.atan2(dy, dx)
	a2 = return_angle(L1, L4, c)

	thetaR = math.floor(a1 - a2)
	# servo3.writeMicroseconds(floor(((a1 - a2) * SERVOFAKTORRIGHT) + SERVORIGHTNULL));

	print(thetaL, thetaR)

set_XY(75, 138)