from robotic_arm_v2 import RoboticArm
from camera_detection import CameraDetection
from collections import defaultdict, Counter
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
        
        while self.camera.get_balls_target(print_target=False) is None : time.sleep(1)

        ball_catch_sequence, catch_bool_data, color_dic, sequence_idx = self.get_sequence()

        print("ball sequence : ", ball_catch_sequence)
        self.control.move_mid()
        self.control.press_buzzer()

        for idx, (ball_info, catch_bool) in enumerate(zip(ball_catch_sequence,catch_bool_data)):
            print("현재 공 : ", ball_info[1])
            print("공 색 : ",ball_info[0])
            print("확인 여부 :,", catch_bool)

            if catch_bool:
                color_result = self.check_error_ball(ball_info[1])
                split_list = color_result.split("_")
                error_check = split_list[-1]
                color = split_list[0]
                if error_check != "error":
                    ball_catch_sequence[sequence_idx.index(color_dic[color])][0] = color + "_error"
            else:
                self.control.move_ball_to_target(ball_info[1],ball_info[0])
             
        self.control.press_buzzer(start_idx=1)

        self.camera.stop()
        return 0    

    def get_sequence(self):
        sort_sequence = [] # 새로운 Sequence 리스트를 생성하기 위한 LIST
        used_indices = [] # 조합되지 않은 공을 위한 LIST

        # 조합되지 않은 공 중 하나의 공만 정밀 작업하기 위한 스위치
        color_modes = {'red': 'mode1', 'green': 'mode1', 'blue': 'mode1'}

        target_list = self.camera.get_balls_target(print_target=False)

        # 각 색상에 대해 조합된 공들을 찾고 target_list에서 정렬
        for color in ['red', 'green', 'blue']:
            indices, found = self.find_and_store_indices(color, target_list)
            if found:
                # 조합된 공이 있을 경우, normal은 맨 앞에, error는 맨 뒤에 추가
                normal_ball = [color, indices[0][1], 'mode1']  # (색깔, 인덱스, mode1)
                error_ball = [color+"_error", indices[1][1], 'mode1']   # (색깔, 인덱스, mode1)
                sort_sequence.insert(0, normal_ball)
                sort_sequence.append(error_ball)
                used_indices.extend([indices[0][1], indices[1][1]])  # 사용된 인덱스 기록
            else:
                pass
        
        color_dic = {}

        # 확인되지 않은 공들을 찾아서 sort_sequence에 추가
        for i in range(len(target_list)):
            if i not in used_indices:
                color_info = target_list[i]
                color = color_info.split('_')[0]  # 색상 추출
                
                if color_modes[color] == 'mode1':
                    sort_sequence.insert(0,[color, i, 'mode1'])  # 조합되지 않은 공 추가
                    color_modes[color] = 'mode2'  # 다음 동일 색상은 mode1로 설정
                    color_dic[color] = i     

                elif color_modes[color] == 'mode2':
                    sort_sequence.insert(0,[color, i, 'mode2'])  # 이미 확인된 동일 색상 공을 mode1로 추가

                else :
                    pass
                
        sequence_idx = []
        for i in sort_sequence:
            sequence_idx.append(i[1])

        mode_boolean_list = [False if mode == 'mode1' else True for _, _, mode in sort_sequence]
        return sort_sequence, mode_boolean_list, color_dic, sequence_idx
    
    def checking_error(self, ball_num):
        self.control.move_mid()
        self.control.grep_ball(ball_num)
        self.control.move_mid()

        count_error = defaultdict(int)  # 간단한 카운팅용 객체

        while self.camera.get_grep_ball_target(print_grep_ball = True) is None: pass
        
        for angle in range(-175,6,30):
            self.control.spin_pump_on_mid(angle)
            grep_ball = self.camera.get_grep_ball_target(print_grep_ball = True)

            if grep_ball is None:
                continue

            count_error[grep_ball] += 1
            if grep_ball.split('_')[-1] == 'error' and count_error[grep_ball] >= 3:
                return grep_ball  # 5번 이상이면 즉시 리턴

        # 'error'로 끝나는 키 중 가장 많이 나온 값 찾기
        error_keys = {key: count for key, count in count_error.items() if key.split('_')[-1] == 'error'}

        if error_keys:
            most_common_error_key = max(error_keys.items(), key=lambda x: x[1])
            
            # 5번 이상 나왔으면 그 값을 리턴
            if most_common_error_key[1] >= 5:
                print("확인 결과 :", most_common_error_key[0])
                return most_common_error_key[0]

        # 그 외의 경우 전체에서 가장 많이 나온 값을 리턴
        if count_error:
            most_common_grep_ball = max(count_error.items(), key=lambda x: x[1])
            print("확인 결과 :", most_common_grep_ball[0])
            return most_common_grep_ball[0]
        else:
            return None
        
    def check_error_ball(self,ball_num):
        while self.camera.get_balls_target(print_target=False) is None : time.sleep(1)
        target_box = self.checking_error(ball_num)
        self.control.move_mid()
        self.control.drop_target_box(target_box)
        self.control.move_mid()

        return target_box

    def find_and_store_indices(self, color, target_list):
        normal_label = f'{color}'
        error_label = f'{color}_error'

        indices = []

        if (normal_label in target_list) and (error_label in target_list):
            normal_idx = target_list.index(normal_label)
            error_idx = target_list.index(error_label)
            indices = [(color, normal_idx, 'normal', 'mode1'), (color, error_idx, 'error', 'mode1')]
                    
            return indices, True
        
        else:
            return None, False

model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_2nd\\detect\\train\\weights\\best.pt'
# model_path = 'C:\\Users\\k-factory\\Desktop\\METAROBO_ARM\\model\\runs_1n2\\detect\\train\\weights\\best.pt'
def main():
    metarobo = Metarobo()
    metarobo.start()

    
    
if __name__ == '__main__':
    main()