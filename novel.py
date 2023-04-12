
from math import cos
from math import sin
from math import atan2
from math import sqrt
from math import pow
from math import acos

l1 = 80
l2 = 80
l3 = 120
l4 = 120
l5 = 30
l6 = 80

q1 = 90
q2 = 90

xa = l2 * cos(q1) - (l6 / 2)
ya = l2 * sin(q1)
xb = l1 * cos(q2) + (l6 / 2)
yb = l1 * sin(q2)

h = sqrt(pow(yb - ya, 2) + pow(xb - xa, 2))



xd = xa + l4 * cos(a1) + l5 * cos(a2)
yd = ya + l4 * sin(a1) + l5 * sin(a2)

xc = xd - l5 * cos(a2)
yc = yd = l5 * sin(a2)

psi = atan2(yd - yc, xd - xc)





a1 = s1 + psi
a2 = pi - (a1 - 2 * psi)



s1 = atan2(yc, xc + (l6 / 2))
s2 = atan2(yc, xc - (l6 / 2))









k1 = sqrt(pow(xc + (l6 / 2), 2) + pow(yc, 2))
k2 = sqrt(pow(xc - (l6 / 2), 2) + pow(yc, 2))

r1 = acos((pow(l2, 2) + pow(k1, 2) - pow(l4, 2)) / (2 * l2 * k1))
r2 = acos((pow(l1, 2) + pow(k2, 2) - pow(l3, 2)) / (2 * l1 * k2))


print(a1, a2)