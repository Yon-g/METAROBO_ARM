from robotic_arm_v2 import RoboticArm

c = RoboticArm()

c.mc.set_encoders_drag([2215, 2399, 1920, 2069, 2820, 310],[300,300,300,300,300,300])
print(c.mc.is_moving())
while c.mc.is_moving() != 0:
    print(c.mc.is_moving())
    print(c.mc.is_moving())
    print(c.mc.is_moving())
    print(c.mc.is_moving())
    print(c.mc.is_moving())
    print(c.mc.is_moving())
    print(c.mc.is_moving())