import cv2
import tkinter as tk
from tkinter import ttk
import re
from pymycobot import MechArm 
import time

mc = MechArm('COM4',115200)

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

# cap = cv2.VideoCapture(1)

# 저장된 로봇 명령어를 저장할 리스트
commands = []
codes = []

#초기 조건들
distance = 15
speed = [1000,1000,1000,1000,1000,1000]
d_speed = [100,100,100,100,100,100]
# speed = 50

def select_distance(dis_entry): # 한칸 거리 지정
    global distance
    distance = int(dis_entry.get())  # 입력된 값을 정수로 변환하여 distance 변수에 할당
    distance_label.config(text=f"움직이는거리: {distance}")  # distance_label 업데이트

def select_speed(spd_entry): # Set The Speed
    global speed
    input_value = spd_entry.get()
    if ',' in input_value:
        speed = [int(val) for val in input_value.split(',')]  # 쉼표로 분리된 값을 리스트로 저장
    else:
        speed = [int(input_value)] * 6  # 입력 값이 하나라면 6축에 동일한 속도 적용
    speed_label.config(text=f"속도: {speed}")  # speed_label 업데이트

def open_new_window(): # 로봇지정및 listbox 창
    global listbox, distance_label, speed_label, codebox  # listbox,distance label를 전역 변수로 선언
    # 새 창 생성
    new_window = tk.Toplevel(root)
    new_window.title("코드 및 로봇 지정")

    # Listbox 생성 및 배치
    listbox = tk.Listbox(new_window, width=50)
    listbox.grid(row=5, column=0)  # grid를 사용하여 배치
    codebox = tk.Listbox(new_window, width=50)
    codebox.grid(row=5, column=1)  # grid를 사용하여 배치

    # 움직이는 거리 Entry 위젯
    distance_label = ttk.Label(new_window, text=f"움직이는 거리: {distance}")
    distance_label.grid(row=3, column=0, padx=5, pady=5)
    distance_entry = ttk.Entry(new_window)
    distance_entry.grid(row=3, column=1, padx=5, pady=5)

    # "적용" 버튼
    apply_button = ttk.Button(new_window, text="적용", command=lambda: select_distance(distance_entry))
    apply_button.grid(row=3, column=2, padx=5, pady=5)

    # 속도 Entry 위젯
    speed_label = ttk.Label(new_window, text=f"속도: {speed}")
    speed_label.grid(row=4, column=0, padx=5, pady=5)
    speed_entry = ttk.Entry(new_window)
    speed_entry.grid(row=4, column=1, padx=5, pady=5)

    # "적용" 버튼
    apply_button = ttk.Button(new_window, text="적용", command=lambda: select_speed(speed_entry))
    apply_button.grid(row=4, column=2, padx=5, pady=5)

def save_position():  # 저장 기능
    respon = mc.get_encoders()  # 로봇의 엔코더 값 가져오기
    commands.append(respon)  # 엔코더 값 저장
    codes.append(speed.copy())  # 현재 속도 값을 복사하여 저장 (리스트로 저장)
    update_listbox()  # Listbox 업데이트
    
def update_listbox(): 
    # Listbox 초기화
    listbox.delete(0, tk.END)
    codebox.delete(0, tk.END)
    
    for i, cmd in enumerate(commands):
        listbox.insert(tk.END, f"{cmd}")       # 엔코더 값 리스트에 추가
        codebox.insert(tk.END, f"{codes[i]}")  # 속도 값 리스트에 추가


def delete_command(): 
    # 선택된 명령어의 인덱스 가져오기
    selected_index = listbox.curselection()
    if selected_index:
        # 선택된 명령어 삭제
        del commands[selected_index[0]]
        del codes[selected_index[0]]  # codebox에서도 해당 항목 삭제
        update_listbox()
    # codebox에서 선택된 인덱스 삭제
    selected_index_codebox = codebox.curselection()
    if selected_index_codebox:
        del codes[selected_index_codebox[0]]
        del commands[selected_index_codebox[0]]  # listbox에서도 해당 항목 삭제
        update_listbox()


def execute_commands_one_by_one(): 
    try:
        start_time = time.time()  # 실행 시작 시간 기록
        for i, cmd in enumerate(commands):
            if isinstance(cmd, str):
                if cmd == "pump_on()":
                    exe_pump_on(commands[i-1])
                
                elif cmd == "pump_off()":
                    mc.pump_off()
            else:
                mc.set_encoders_drag(cmd, codes[i])  # 해당 명령어에 맞는 속도 적용
            print(f"Command: {cmd}, Speed: {codes[i]}")
            
            while mc.is_moving():
                time.sleep(0.1)  # 0.1초 딜레이
            time.sleep(0.3)  # 0.3초 딜레이
            
        end_time = time.time()  # 실행 종료 시간 기록
        elapsed_time = end_time - start_time  # 실행 시간 계산
        print(f"All commands executed in {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Error executing command: {e}")

def copy_commands(): # 리스트박스 복사 및 출력
    # Listbox에 저장된 내용을 가져옵니다.
    commands_text = [listbox.get(idx) for idx in range(listbox.size())]
    print('동작코드 시작\n')

    # 가져온 내용을 한 줄씩 출력합니다.
    for cmd in commands_text:
        print(cmd)
    print('\n동작코드 종료')
   
def exe_pump_on(target_joint): # 만들어진 시퉌스를 실행할 때
    # target_pos = target_joint
    cur_pos = mc.get_encoders()
    move_complete = True

    while move_complete:
        good_for = False
        for i in range(len(target_joint)):
            print("조인트",i,"번 차이 :",target_joint[i] - cur_pos[i])
            if abs(target_joint[i] - cur_pos[i]) >= 15:
                print(f"차이가 15 이상cur_pos준: {target_joint[i]}, cur_pos: {cur_pos[i]}")
                mc.set_encoders_drag(target_joint,d_speed)
                time.sleep(0.1)
                good_for = True
                break
        if not good_for:
            move_complete = False
            print("도착")
    time.sleep(0.5)
    mc.pump_on()
    while mc.is_moving():
        time.sleep(0.01)

def pump_on(): #시퀀스를 만들때 - 손으로 조작할때
    temp_pos = mc.get_encoders()
    mc.pump_on()

    commands.append('pump_on()')
    codes.append(d_speed)

    while mc.is_moving():
        time.sleep(0.01)


def pump_off():
    mc.pump_off()

    commands.append('pump_off()')
    codes.append(d_speed)

def servo_on():
    mc.power_on()

def servo_off():
    mc.release_all_servos()

root = tk.Tk()

button_state = tk.IntVar() # 버튼의 상태를 나타내는 변수


def move(axis, direction):
    # 현재 로봇의 엔코더 값을 가져옴
    encoders = mc.get_encoders()
    # encoders = mc.get_coords()
    print(direction)
    if direction == "+":
        distance_value = distance
    elif direction == "-":
        distance_value = -distance
    print("init_pose",encoders)
    print(type(encoders))
    print("distance",distance_value)
    print(axis)
    # 각 축별로 이동할 때, 해당 축에 distance_value를 더함
    if axis == "j1":
        encoders[0] += distance_value  # 1 축 이동
    elif axis == "j2":
        encoders[1] += distance_value  # 2 축 이동
    elif axis == "j3":
        encoders[2] += distance_value  # 3 축 이동
    elif axis == "j4":
        encoders[3] += distance_value  # 4 축 회전
    elif axis == "j5":
        encoders[4] += distance_value  # 5 축 회전
    elif axis == "j6":
        encoders[5] += distance_value  # 6 축 회전
    print("input",encoders)
    # 새로운 엔코더 값으로 로봇을 이동
    mc.set_encoders_drag(encoders, speed)
    # mc.send_coords(encoders, speed)
    while mc.is_moving():
        print("움직이는중",end="")
        time.sleep(0.01)
    encoders = mc.get_encoders()
    print("output",encoders)

    # 이동 후 잠시 대기
    time.sleep(0.1)


#여기부터 버튼배치-----------------------------------------------

# x+, x-, y+, y- 등등 버튼
move_buttons = []

# 방향 리스트
directions = ["+", "-"]

button_texts = ["j1+", "j1-", "j2+", "j2-", "j3+", "j3-", "j4+", "j4-", "j5+", "j5-", "j6+", "j6-"]
for i, text in enumerate(button_texts):
    axis = text[:2]
    button = tk.Button(root, text=text, command=lambda idx=i, axis=axis: move(axis, "+" if idx % 2 == 0 else "-"), width=5)
    button.grid(row=i//2, column=i%2,padx = 5 ,pady=5)
    move_buttons.append(button)


# "Save" 버튼
save_button = tk.Button(root, text="저장", command=save_position)
save_button.grid(row=1, column=3, pady=10)

# "Delete" 버튼
delete_button = tk.Button(root, text="삭제", command=delete_command)
delete_button.grid(row=1, column=4, pady=10)

# "Servo on" 버튼
servo_button = tk.Button(root, text="서보 고정 풀기", command=servo_off)
servo_button.grid(row=10, column=5, pady=10)

# "Servo off" 버튼
servo_button = tk.Button(root, text="서보 고정", command=servo_on)
servo_button.grid(row=10, column=6, pady=10)

# 모두 실행 버튼
execute_one_by_one_button = tk.Button(root, text="모두 실행", command=execute_commands_one_by_one)
execute_one_by_one_button.grid(row=0, column=3,padx = 5,  pady=10)

# "Copy" 버튼
copy_button = tk.Button(root, text="복사용 코드 생성", command=copy_commands)
copy_button.grid(row=2, column=3,padx = 5, pady=10)

# 메시지 표시 레이블
message_label = tk.Label(root, text="")
message_label.grid(row=3, column=0, columnspan=4)

# "새 창 열기" 버튼
open_button = tk.Button(root, text="저장된 코드 및 COM 포트 연결", command=open_new_window)
open_button.grid(row=9, column=5, columnspan=4, pady=10) 


# 펌프 on 버튼 생성
button = tk.Button(root, text="pump on", command=pump_on)
button.grid(row=7, column=1)

# 펌프 off 버튼 생성
button = tk.Button(root, text="pump off", command=pump_off)
button.grid(row=7, column=2)

open_new_window()

import threading

# def video_writer():
#     cap = cv2.VideoCapture(1)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
#     while True:
#         print("캡처 실행중")
#         ret, frame = cap.read()
#         # cv2.imshow('frame', frame)
#         time.sleep(0.1)
#         out.write(frame)

# video_thread = threading.Thread(target=video_writer)
# video_thread.start()
root.mainloop()
# video_thread.join()