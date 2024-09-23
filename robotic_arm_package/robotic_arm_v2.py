import json
import os
import time
from pymycobot import MechArm 

BALL_OVER = 0 #공 
BALL_CATCH = 1
BALL_LIFT = 2

ENCODER = 0
ANGLE = 1

BALL_KEY = {
    "blue" : "BLUE",
    "blue_error" : "ERROR",
    "green" : "GREEN",
    "green_error" : "ERROR",
    "red" : "RED",
    "red_error" : "ERROR",
}

class RoboticArm:
    def __init__(self, com_n = 4, move_point_json = 'move_point.json'):
        """
        Initializes the RoboticArm class. Establishes communication with the MechArm robot through a COM port 
        and loads movement points from a JSON file.
        
        Args:
        com_n (int): The COM port number to connect to the robotic arm.
        move_point_json (str): The name of the JSON file containing movement points.
        """
        print("Init RoboticArm")
        self.mc = MechArm('COM'+str(com_n),115200)
        self.arm_point = None
        self.error_count = 0
        self.read_json(move_point_json)

    def read_json(self, move_point_json): 
        """
        Reads the movement point data from a JSON file and stores it in the arm_point attribute.

        Args:
        move_point_json (str): The name of the JSON file containing movement points.
        """
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir,'param\\')
        with open(config_path+move_point_json, "r", encoding='utf-8-sig') as f:
            self.arm_point = json.load(f)
            print("Read json")

    def moving_cmd(self, target, idx, motor_mode):
        """
        Moves the robotic arm based on the given target points and motor mode (ENCODER or ANGLE).

        Args:
        target (dict): The target points for the robotic arm.
        idx (int): The index of the point to move to.
        motor_mode (int): The motor mode to use (ENCODER or ANGLE).
        """
        cmd = target["POINT"][idx] # read target point
        speed = target["SPEED"][idx] # read target speed

        if motor_mode == ENCODER:
            cmd[-1] = 3737 # fix last index value 
            self.mc.set_encoders_drag(cmd,speed) # send commands in encoder mode
        elif motor_mode == ANGLE:
            cmd[-1] = -148.44 # fix last index value 
            self.mc.send_angles(cmd,speed) # send commands in angle mode

        time.sleep(0.3)
        while self.mc.is_moving() != 0: 
            pass

    def move_mid(self):
        """
        Moves the robotic arm to the middle position.
        """
        mid = self.arm_point["MID"] # read mid point dictionary
        self.moving_cmd(mid,BALL_OVER,ANGLE) # move to mid while holding the ball

    def grep_ball(self, ball_num): 
        """
        Moves the robotic arm to grab a ball from a specified position and lift it.

        Args:
        ball_num (int): The number of the ball to grab (1, 2, 3, etc.).
        """
        ball = self.arm_point["BALL"+str(ball_num)] # read ball dictionary

        self.moving_cmd(ball,BALL_OVER,ENCODER) # move on ball
        print("ball:",ball_num)
        print("encoder:",self.mc.get_encoders())
        self.mc.pump_on() # pump on
        self.moving_cmd(ball,BALL_CATCH,ENCODER) # go down to catch ball
        self.moving_cmd(ball,BALL_LIFT,ENCODER) # lift ball
        print("--------")


    def drop_target_box(self, target_box):
        """
        Drops the ball into the target box, or if the target box is marked as "ERROR", 
        drops it in an error location.

        Args:
        target_box (str): The target box where the ball should be dropped ("RED", "BLUE", "ERROR", etc.).
        """
        target_box = BALL_KEY[target_box]
        if target_box == "ERROR": # if it's the error ball, bring a point in the current error count order
            target = self.arm_point["ERROR" + str(self.error_count)]
            self.error_count += 1
        else: # if it's not the wrong ball, read a box that matches the color
            target = self.arm_point[target_box]
        
        if target_box == "ERROR": # save pump off timing
            put_idx = len(target["POINT"])-2
        else:
            put_idx = 0

        for idx in range(len(target["POINT"])):
            if idx == put_idx:
                self.mc.pump_off()
            self.moving_cmd(target, idx, ANGLE)

    def move_ball_to_target(self, ball_num, target_box):
        """
        Moves the ball from its starting position to a target box.

        Args:
        ball_num (int): The number of the ball to move (1, 2, 3, etc.).
        target_box (str): The target box where the ball should be moved ("RED", "BLUE", etc.).
        """
        self.move_mid() # move mid
        self.grep_ball(ball_num) # grep ball 
        self.move_mid() # move mid
        self.drop_target_box(target_box) # move target box and drop the ball

    def press_buzzer(self):
        """
        Moves the robotic arm to press a buzzer.
        """
        self.move_mid()

        botton = self.arm_point["BUZZER"]

        for idx in range(len(botton["POINT"])):
            self.moving_cmd(botton, idx, ENCODER)

    def spin_pump_on_mid(self, angle):
        """
        Spins the pump to a specific angle while in the middle position.

        Args:
        angle (float): The angle to rotate to.
        """
        mid = self.arm_point["MID"]
        cmd = mid["POINT"][BALL_OVER]
        speed = mid["SPEED"][BALL_OVER]

        cmd[-1] = angle
        self.mc.send_angles(cmd, speed)
        time.sleep(0.3)
        while self.mc.is_moving() != 0: 
            pass

if __name__ == "__main__":
    robot = RoboticArm(com_n=4, move_point_json='move_point_v2.json')

    robot.move_ball("BALL0","RED")
    robot.move_ball("BALL3","BLUE")
    robot.move_ball("BALL4","GREEN")
