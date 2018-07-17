import math
#------------------- Import from PyDimitri ---------------------
import sys
import numpy as np
from PyDimitri import Joint, DxlComm
import time 
#--------------------- Set Perna -------------------------------
idmotors = [13,15,17,19,21,23]
setAngle = [4.59,5.37,1.11,5.25,6.21,0.73]
joints = [Joint(mid) for mid in idmotors]

port = DxlComm('/dev/ttyUSB0', 1)

port.attachJoints(joints)
i = 0
#while True:
for j in joints:
    j.setGoalAngle(setAngle[i])
    print(setAngle[i])
    i += 1
port.sendGoalAngles()

time.sleep(3)

#------------------ Set Sensor ---------------------------------
motor_id = int(104)
j1 = Joint(motor_id)
#------------------ Define port --------------------------------
port.attachJoint(j1)



# Use first 30 or so measures to calibrate the center value
print("Calibrating...")
values = []
for i in range(300):
	values.append(j1.receiveSEA())
j1.setCenterValue(np.mean(values))
print('primeiro valor: ', j1.receiveSEA())
aux = j1.receiveSEA()

#------------------------------------------------------------

import time
import numpy as np
r = np.float128(aux)
y = np.float128(aux)
e1 = np.float128(0)
e1l = np.float128(0)
u1 = np.float128(0)
u2 = np.float128(0)
u3 = np.float128(0)
u1l = np.float128(0)
u2l = np.float128(0)
u3l = np.float128(0)
u3l2 = np.float128(0)
up = np.float128(0)
upl = np.float128(0)
a1 = np.float128(-2.973571)
a2 = np.float128(0.339894)
a3 = np.float128(1.011383)
ap = np.float128(-0.00184751)
b1 = np.float128(-2.973571)
b2 = np.float128(-0.329785)
b3 = np.float128(-0.988594)
bp = np.float128(-0.00369502)
c1 = np.float128(0.944941)
c2 = np.float128(0.330319)
c3 = np.float128(-0.999978)
cp = np.float128(-0.00184751)
ep = np.float128(-1.98764586)
fp = np.float128(0.98873263)

start = time.time()
a = 0.
b = 0.
i = 0

import csv
file = open('caso.csv', 'w')
writer = csv.writer(file)

while True:
    i += 1

    e1l = e1
    e1 = r - y
    print('erro', e1, e1l)

    u1l = u1
    u1 = -c1*u1l + a1*e1 + b1*e1l
    #print('u1', u1, u1l)

    u2l = u2
    u2 = -c2*u2l + a2*u1 + b2*u1l
    #print('u2', u2, u2l)

    u3l2 = u3l
    u3l = u3
    u3 = -c3*u3l + a3*u2 + b3*u2l
    print('control', u3, u3l, u3l2)

    # upl2 = upl
    # upl = up
    # up = -ep*upl -fp*upl2 + ap*u3 + bp*u3l + cp*u3l2
    # print('planta', up, upl, upl2)

    # # if (x > 0):
    # #     y = 240 + up
    # # if (x == 0):
    # #     y = 247 + up

    #--------------------------------------------
    # y = up
    print('referencia', r)
    #print('goal', aux)
    y = j1.receiveSEA()
    print('planta', y)
    writer.writerow([i,y])
    e_rad = round(u3*math.pi/180.,5)
    print('rad',e_rad)
    
    # ik = 0
    # for j in joints:
    #     j.setGoalAngle(setAngle[ik] + e_rad)
    #     print(setAngle[ik]+e_rad)
    #     ik += 1
    
    for ik, j in enumerate(joints):
        if (ik < 4):
            a = setAngle[ik] + e_rad
            #print(type(a))
            j.setGoalAngle(a)
            print(ik,setAngle[ik]+e_rad)
        if (ik >= 4):
            a = setAngle[ik]
            j.setGoalAngle(a)
            print(ik,setAngle[ik])
    port.sendGoalAngles()
    #print('saida -------------------------->',y)