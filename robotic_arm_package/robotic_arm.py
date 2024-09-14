import json
import os
import time
from pymycobot import MechArm 

BALL_OVER = 0
BALL_CATCH = 1
BALL_LIFT = 2

ENCODER = 0
ANGLE = 1

class RoboticArm:

    def __init__(self, com_n = 4, move_point_json = 'move_point.json'):
        print("Init RoboticArm")

        self.mc = MechArm('COM'+str(com_n),115200)

        self.arm_point = None
        self.read_json(move_point_json)

    def read_json(self, move_point_json):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir,'param\\')
        with open(config_path+move_point_json, "r", encoding='utf-8-sig') as f:
            self.arm_point = json.load(f)
            print("Read json")
            print(self.arm_point["BALL0"])

    def move_ball(self, ball_num, target_box):
        ball = self.arm_point[ball_num]
        action = ball["CATCH"]
        self.moving_cmd(action,BALL_OVER,ENCODER)
        self.mc.pump_on()
        self.moving_cmd(action,BALL_CATCH,ENCODER)
        self.mc.pump_off()
        self.moving_cmd(action,BALL_LIFT,ENCODER)

        action = ball[target_box]
        for idx in range(len(action["POINT"])):
            self.moving_cmd(action,idx,ANGLE)
            print("옮겨!")

    def moving_cmd(self, action, idx, motor_mode):
        if motor_mode == ENCODER:
            cmd = action["POINT"][idx]
            speed = action["SPEED"][idx]
            self.mc.set_encoders_drag(cmd,speed)

        elif motor_mode == ANGLE:
            cmd = action["POINT"][idx]
            speed = action["SPEED"][idx]
            self.mc.send_angles(cmd,speed)

        time.sleep(0.3)
        while self.mc.is_moving() != 0: 
            pass

if __name__ == "__main__":
    robot = RoboticArm(com_n=7, move_point_json='move_point.json' )

    robot.move_ball("BALL0","RED")