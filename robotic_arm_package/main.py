from robotic_arm_v2 import RoboticArm
from camera_detection import CameraDetection
import time

class Metarobo:

    def __init__(self):
        self.control = RoboticArm(com_n=4, move_point_json='move_point_v2.json')
        self.camera = CameraDetection(1,model_path)
        self.camera.start()

    def start(self):
        start_signal = int(input())
        print("start: 1, break : another")
        if start_signal != 1:
            return 0
        
        ball_catch_sequence = [0,1,2,3,4,5]
        sequence_idx = 0

        while self.camera.get_balls_target(print_target=False) is None : time.sleep(1)

        self.control.press_buzzer()

        while sequence_idx < 6:
            target_list = self.camera.get_balls_target(print_target=False)
            greb_ball = self.camera.get_grep_ball_target(print_grep_ball=False)
            print(target_list)

            ball_num = ball_catch_sequence[sequence_idx]
            target_box = target_list[ball_num]

            self.control.move_ball(ball_num,target_box)

            sequence_idx+=1

        self.control.press_buzzer()

        self.camera.stop()
        return 0    

    def checking_error(self, ball_num):
        self.control.move_mid(ball_num)

        not_error = 0
        error = 0

        while self.camera.get_grep_ball_target(print_grep_ball = True) is None: pass
        
        for angle in range(-175,177,10):
            self.control.spin_pump_on_mid(angle)
            grep_ball = self.camera.get_grep_ball_target(print_grep_ball = True)

            if grep_ball == "ERROR":
                error+=1
            else:
                not_error+=1
        print("검사 결과 : ",not_error,error)

    def mid_check(self):
        self.camera.start()
        while self.camera.get_balls_target(print_target=False) is None : time.sleep(1)
        print("시작")
        self.checking_error(3)
        

model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_2nd\\detect\\train\\weights\\best.pt'
# model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_1n2\\detect\\train\\weights\\best.pt'
def main():
    metarobo = Metarobo()
    metarobo.start()
    
    
if __name__ == '__main__':
    main()