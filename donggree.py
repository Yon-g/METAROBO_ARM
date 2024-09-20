from pymycobot import MechArm
import time

mc = MechArm('COM4',115200)


# Set of speed 

s = 100
ls =20

#Point of o(default) 

A0 = [-15.9, 37.17, -19.68, 0.96, 71.8, -153.63]
A1 = [-16.52, 36.91, -5.09, -0.08, 55.37, -153.63]

#Point of 1

B0 = [-2.1, 32.34, -7.11, 3.51, 64.95, -158.9]
B1 = [-2.28, 37.7, -7.03, 3.25, 61.61, -160.66]

# Point of 2(default)

C0 = [17.66, 33.39, -10.72, 1.14, 64.07, -128.84]
C1 = [17.4, 32.95, 0.7, 0.08, 50.97, -128.75]

# Point of 3

D0 = [-23.46, 12.3, 16.08, 0.79, 60.38, -147.74]
D1 = [-23.37, 19.07, 18.63, -0.35, 54.49, -147.83]

# Point of 4

E0 = [2.19, 7.2, 20.21, 0.43, 63.63, -155.91]
E1 = [1.84, 17.66, 20.47, -0.87, 57.56, -156.62]

# Point of 5

F0 = [21.79, 7.47, 20.91, 2.98, 58.71, -156.53]
F1 = [22.5, 17.31, 19.95, 2.1, 53.61, -156.7]

# point of middle up 

mid = [7.11, -4.39, -12.48, -2.54, 94.92, -156.62]

#green end
gr0 = [-45.26, -7.2, -0.17, 4.57, 75.76, -156.62]
gr1 = [-29.09, 19.07, -20.65, -37.61, 86.48, -156.62]
gr2 = [-3.6, 24.08, 8.43, -36.21, 67.06, -156.62]

#blue end

bl0 = [-17.75, -2.98, -13.18, -1.93, 85.86, -101.68]
bl1 = [-68.9, -0.52, -3.6, -31.2, 85.86, -101.68]
bl2 = [-65.12, -6.85, 21.79, -17.75, 85.86, -101.68]

#error end

erstart = [15.64, 19.24, -2.1, 2.81, 62.92, -134.38]
er0 = [30.93, 36.65, -41.57, 2.81, 71.45, -134.38]
er01 = [30.93, 3.16, 10.72, 2.81, 3.6, -134.38]
er1 = [30.93, 40.42, -10.19, 2.81, 3.6, -134.38]
er2 = [30.93, 14.85, 24.52, 2.81, 3.6, -134.38]

def working():
    mc.send_angles(mid, s)
    time.sleep(1)
    mc.send_angles(A0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(A1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(A0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(B0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(B1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(B0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(C0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(C1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(C0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(D0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(D1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(D0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(E0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(E1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(E0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(F0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(F1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(F0,s)
    time.sleep(1)
    mc.send_angles(mid,s)
    time.sleep(1)

    mc.send_angles(A0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(A1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(gr1,s)
    time.sleep(1)
    mc.send_angles(gr2,s)
    time.sleep(1)

    mc.send_angles(mid,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(B1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(er1,s)
    time.sleep(1)
    mc.send_angles(er2,s)


def gr():

    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(A0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(A1,ls)
    time.sleep(1)
    mc.pump_off()
    mc.send_angles(gr0,s)
    time.sleep(1)
    mc.send_angles(gr1,s)
    time.sleep(1)
    mc.send_angles(gr2,s)
    time.sleep(1)

def er():
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(C0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(C1,ls)
    time.sleep(1)
    mc.send_angles(erstart,s)
    mc.pump_off()
    # mc.send_angles(er0,s)
    time.sleep(0.5)
    mc.send_angles(er01,s)
    time.sleep(0.5)
    mc.send_angles(er1,s)
    time.sleep(0.5)
    mc.send_angles(er2,s)
    time.sleep(1)

def blue():
    mc.send_angles(mid,s)
    time.sleep(1)
    mc.send_angles(A0,s)
    time.sleep(1)
    mc.pump_on()
    mc.send_angles(A1,ls)
    time.sleep(1)
    mc.send_angles(bl0,s)
    mc.pump_off()
    # mc.send_angles(er0,s)
    time.sleep(1)
    mc.send_angles(bl1,s)
    time.sleep(1)
    mc.send_angles(bl2,s)
    time.sleep(1)






#working()
# er()
# er()
# er()
er()
gr()
blue()