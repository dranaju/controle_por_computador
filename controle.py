import math
#------------------- Import from PyDimitri ---------------------
import sys
import numpy as np
from PyDimitri import Joint, DxlComm
import time 

port = DxlComm('/dev/ttyUSB0', 1)
#----------------------- Set foot ---------------------------------
idmotors1 = [21,23]
setAngle1 = [6.22,0.83]
joints1 = [Joint(mid1) for mid1 in idmotors1]
port.attachJoints(joints1)
i = 0
for j in joints1:
	j.enableTorque()
for j in joints1:
    j.setGoalAngle(setAngle1[i])
    print(setAngle1[i])
    i += 1
port.sendGoalAngles()
#--------------------- Set joelho -------------------------------
idmotors = [13,15,17,19]
setAngle = [4.32,5.11,1.24,5.37]
joints = [Joint(mid) for mid in idmotors]

port.attachJoints(joints)
i = 0
# for j in joints:
# 	j.enableTorque()
for j in joints:
    j.setGoalAngle(setAngle[i])
    print(setAngle[i])
    i += 1
port.sendGoalAngles()
#------------------------------------------------------------------

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
ganho = 1.0
tempo_step = 2
while True:
    i += 1

    e1l = e1
    e1 = r - y
    print('erro', e1, e1l)

    u1l = u1
    u1 = -c1*u1l + a1*e1 + b1*e1l
    u1 = u1*ganho
    #print('u1', u1, u1l)

    u2l = u2
    u2 = -c2*u2l + a2*u1 + b2*u1l
    u2 = u2*ganho
    #print('u2', u2, u2l)

    u3l2 = u3l
    u3l = u3
    u3 = -c3*u3l + a3*u2 + b3*u2l
    u3 = u3*ganho
    print('control', u3, u3l, u3l2)
    
    #--------------------------------------------
    # y = up
    print('referencia', r)
    #print('goal', aux)
    y = j1.receiveSEA()
    if (y > 0):
        yl = y
    if (y == 0.0):
        y = yl
    print('planta', y)
    writer.writerow([i,y])
    e_rad = round(u3*math.pi/180.,5)
    #print('rad',e_rad)
    
    if (i%5000 != 0):
        for ik, j in enumerate(joints):
            if (ik < 2):
                a = setAngle[ik] - e_rad
                #print(type(a))
                j.setGoalAngle(a)
                print(ik,a)
                # print(ik,setAngle[ik])
                print(ik,setAngle[ik])
            #print('currente', 13+ 2*ik, j.receiveCurrAngle())
        port.sendGoalAngles()
        time.sleep(0.00001)
    print(i,'-------')
    if (i%5000 == 0 and i != 0):
        print('aaaaaaaaaaaa')
        for ik, j in enumerate(joints):
            if (ik < 2):
                a = setAngle[ik] + (0.17)*5
                j.setGoalAngle(a)
                print(ik, a)
            if (ik >= 2):
                a = setAngle[ik] - 0.08
                j.setGoalAngle(a)
                print(ik, a)
            #print('currente', 13+ 2*ik, j.receiveCurrAngle())
        port.sendGoalAngles()
        y = j1.receiveSEA()
        time.sleep(tempo_step)