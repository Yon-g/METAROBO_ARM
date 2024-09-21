import json
import os
import time
from pymycobot import MechArm 

BALL_OVER = 0 #공 
BALL_CATCH = 1
BALL_LIFT = 2

ENCODER = 0
ANGLE = 1

class RoboticArm:
    def __init__(self, com_n = 4, move_point_json = 'move_point.json'):
        print("Init RoboticArm")

        self.mc = MechArm('COM'+str(com_n),115200)

        self.arm_point = None
        self.error_count = 0
        self.read_json(move_point_json)

    def read_json(self, move_point_json):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir,'param\\')
        with open(config_path+move_point_json, "r", encoding='utf-8-sig') as f:
            self.arm_point = json.load(f)
            print("Read json")

    def move_ball(self, ball_num, target_box):
        ball = self.arm_point["BALL"+str(ball_num)]

        if target_box == "ERROR":
            target = self.arm_point["ERROR" + str(self.error_count)]
            self.error_count+=1
        else:
            target = self.arm_point[target_box]

        mid = self.arm_point["MID"]

        self.moving_cmd(mid,BALL_OVER,ANGLE)

        self.moving_cmd(ball,BALL_OVER,ENCODER)
        self.mc.pump_on()
        self.moving_cmd(ball,BALL_CATCH,ENCODER)
        self.moving_cmd(ball,BALL_LIFT,ENCODER)

        self.moving_cmd(mid,BALL_OVER,ANGLE)

        
        if target_box == "ERROR":
            put_idx = len(target["POINT"])-2
        else:
            put_idx = 0

        for idx in range(len(target["POINT"])):
            if idx == put_idx:
                self.mc.pump_off()
            self.moving_cmd(target,idx,ANGLE)

    def moving_cmd(self, action, idx, motor_mode):
        cmd = action["POINT"][idx]
        speed = action["SPEED"][idx]

        if motor_mode == ENCODER:
            cmd[-1] = 3737
            self.mc.set_encoders_drag(cmd,speed)
        elif motor_mode == ANGLE:
            cmd[-1] = -148.44
            self.mc.send_angles(cmd,speed)

        time.sleep(0.3)
        while self.mc.is_moving() != 0: 
            pass

    def press_buzzer(self):
        mid = self.arm_point["MID"]
        self.moving_cmd(mid,BALL_OVER,ANGLE)
        botton = self.arm_point["BUZZER"]

        for idx in range(len(botton["POINT"])):
            self.moving_cmd(botton,idx,ENCODER)

    def move_mid(self,ball_num):
        ball = self.arm_point["BALL"+str(ball_num)]
        mid = self.arm_point["MID"]

        self.moving_cmd(mid,BALL_OVER,ANGLE)

        self.moving_cmd(ball,BALL_OVER,ENCODER)
        self.mc.pump_on()
        self.moving_cmd(ball,BALL_CATCH,ENCODER)
        self.moving_cmd(ball,BALL_LIFT,ENCODER)

        self.moving_cmd(mid,BALL_OVER,ANGLE)

    def spin_pump_on_mid(self,angle):
        mid = self.arm_point["MID"]
        cmd = mid["POINT"][BALL_OVER]
        speed = mid["SPEED"][BALL_OVER]

        cmd[-1] = angle
        self.mc.send_angles(cmd,speed)

        while self.mc.is_moving() != 0: 
            pass

if __name__ == "__main__":
    robot = RoboticArm(com_n=4, move_point_json='move_point_v2.json')

    robot.move_ball("BALL0","RED")
    robot.move_ball("BALL3","BLUE")
    robot.move_ball("BALL4","GREEN")



    
    
    