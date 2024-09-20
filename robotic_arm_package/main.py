from robotic_arm_v2 import RoboticArm
from camera_detection import CameraDetection
import time

model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_2nd\\detect\\train\\weights\\best.pt'
# model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_1n2\\detect\\train\\weights\\best.pt'
def main():
    control = RoboticArm(com_n=4, move_point_json='move_point_v2.json')
    camera = CameraDetection(1,model_path)

    camera.start()

    ball_catch_sequence = [0,1,2,3,4,5]
    sequence_idx = 0

    while camera.get_balls_target(print_target=False) is None : time.sleep(1)

    control.press_buzzer()

    while sequence_idx < 6:
        target_list = camera.get_balls_target(print_target=False)
        greb_ball = camera.get_grep_ball_target(print_grep_ball=False)
        print(target_list)
        
        ball_num = ball_catch_sequence[sequence_idx]
        target_box = target_list[ball_num]

        control.move_ball(ball_num,target_box)

        sequence_idx+=1

    control.press_buzzer()

    camera.stop()
    return 0
    
if __name__ == '__main__':
    main()