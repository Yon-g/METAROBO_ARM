import json
from pymycobot import MechArm 

class RoboticArm:
    def __init__(self):
        print("init arm")

        self.mc = MechArm('COM4',115200)




def main():
    robotic_arm = RoboticArm()

if __name__ == '__main__':
    main()