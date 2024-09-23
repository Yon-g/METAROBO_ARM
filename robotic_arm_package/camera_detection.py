import cv2
import threading
from ultralytics import YOLO
import numpy as np
import math
import time
from collections import defaultdict, Counter

# Load the YOLOv8 trained model

MARGIN = 10
DISTANCE_THRESHOLD = 50

ROI = [
        {"name": "ball0", "x1": 469, "y1": 345, "x2": 549, "y2": 425, "area": 0},
        {"name": "ball1", "x1": 290, "y1": 352, "x2": 370, "y2": 432, "area": 1},
        {"name": "ball2", "x1": 88,  "y1": 353, "x2": 168, "y2": 433, "area": 2},
        {"name": "ball3", "x1": 403, "y1": 247, "x2": 483, "y2": 327, "area": 3},
        {"name": "ball4", "x1": 248, "y1": 245, "x2": 328, "y2": 325, "area": 4},
        {"name": "ball5", "x1": 81,  "y1": 239, "x2": 161, "y2": 319, "area": 5}
    ]

roi_1_coords = (23, 4, 608, 317) # (x1, y1, x2, y2)
roi_2_coords = (31, 321, 593, 471)  # (x1, y1, x2, y2)


class CameraDetection:
    def __init__(self, camera_serial_number = 0, model_path = None):
        print("Init CameraDetection")
        print("Camera Loading")
        self.cap = cv2.VideoCapture(camera_serial_number, cv2.CAP_DSHOW)
        print("Camera Loaded")
        self.ret = False
        self.frame = None
        self.stopped = False

        if model_path is None:
            print("Model is not exist")
        else:
            print("Model Loading...")
            self.model = YOLO(model_path)
            print("Model Loaded")

        self.top_objects_data = defaultdict(lambda: {"labels": Counter(), "coordinates": None})    # 위쪽 구역 객체
        self.bottom_objects_data = defaultdict(lambda: {"labels": Counter(), "coordinates": None})  # 아래쪽 구역 객체

        self.cheked_bottom_balls = [
                None, None, None,
                None, None, None
        ] 
        self.grep_ball = None

    def __del__(self):
        print("Destroy CameraDetection")
    
    def start(self):
        print("starta thread")
        threading.Thread(target=self.update, args=()).start()
        return self
    
    def detection_ball(self, result, roi_x, roi_y, center_y):
        boxes = result.boxes.xyxy.numpy()  # 객체탐지 박스 경계좌표(왼쪽위, 오른아래쪽)
        confidences = result.boxes.conf.numpy()  # 정확도
        class_ids = result.boxes.cls.numpy()  # 클래스 라벨값

        for i, box in enumerate(boxes):
            x1 = int(box[0]) + roi_x
            y1 = int(box[1]) + roi_y
            x2 = int(box[2]) + roi_x
            y2 = int(box[3]) + roi_y
            conf = confidences[i]
            if conf >= 0.50:  # 정확도 50% 이상인지 확인
                cls = int(class_ids[i])
                label = self.model.names[cls]  # 클래스 이름
                
                color = (0, 255, 0)  # 경계박스 색(초록색으로 경계선 생성)
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(self.frame, f"{label} ({conf:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # 객체의 중심 좌표
                center_x = (x1 + x2) // 2
                center_box_y = (y1 + y2) // 2
                new_center = (center_x, center_box_y)

                # 중심선 근처에 걸친 객체는 가장 가까운 구역에 포함
                if center_y - MARGIN <= center_box_y <= center_y + MARGIN:
                    if center_box_y > center_y:
                        if not self.is_near_existing_object(new_center, self.bottom_objects_data, DISTANCE_THRESHOLD):
                            self.bottom_objects_data[center_box_y]["labels"][label] += 1
                            self.bottom_objects_data[center_box_y]["coordinates"] = new_center
                    else:
                        if not self.is_near_existing_object(new_center, self.top_objects_data, DISTANCE_THRESHOLD):
                            self.top_objects_data[center_box_y]["labels"][label] += 1
                            self.top_objects_data[center_box_y]["coordinates"] = new_center
                elif center_box_y < center_y:  # 위쪽에 있는 경우
                    if not self.is_near_existing_object(new_center, self.top_objects_data, DISTANCE_THRESHOLD):
                        self.top_objects_data[center_box_y]["labels"][label] += 1
                        self.top_objects_data[center_box_y]["coordinates"] = new_center
                else:  # 아래쪽에 있는 경우
                    if not self.is_near_existing_object(new_center, self.bottom_objects_data, DISTANCE_THRESHOLD):
                        self.bottom_objects_data[center_box_y]["labels"][label] += 1
                        self.bottom_objects_data[center_box_y]["coordinates"] = new_center
        
    def update(self):
        count = 0

        top_most_common_label = None
        top_coordinates = None
        bottom_most_common_label = None
        bottom_coordinates = None

        while not self.stopped:
            # start = time.time()
            self.ret, self.frame = self.cap.read()
            
            # 프레임 정보 확인
            height, width = self.frame.shape[:2]

            roi_1 = self.frame[roi_1_coords[1]:roi_1_coords[3], roi_1_coords[0]:roi_1_coords[2]]  # 자르기: [y1:y2, x1:x2]
            roi_2 = self.frame[roi_2_coords[1]:roi_2_coords[3], roi_2_coords[0]:roi_2_coords[2]]


            # (화면을 위아래로 나누기 위한 중앙선 설정)
            center_y = height // 2

            results_roi_1 = self.model.predict(roi_1, verbose=False)

            # 모델에 ROI 2 넣기
            results_roi_2 = self.model.predict(roi_2, verbose=False)

            
            results = self.model.predict(self.frame, verbose=False)

            # for result in results:
            #     self.detection_ball(result, height, width, center_y)

            for result in results_roi_1:
                self.detection_ball(result, roi_1_coords[0], roi_1_coords[1], center_y)

            for result in results_roi_2:
                self.detection_ball(result, roi_2_coords[0], roi_2_coords[1], center_y)
            
            count+=1

            if count%10 == 0:
                self.top_objects_data.clear()
                self.bottom_objects_data.clear()
                count = 0

            # 위쪽 구역의 객체 정보 출력
            for obj_key, obj_info in self.top_objects_data.items():
                top_most_common_label, _ = obj_info["labels"].most_common(1)[0]  # 가장 많이 나온 라벨
                top_coordinates = obj_info["coordinates"]
                cv2.putText(self.frame, f"{top_most_common_label}", (top_coordinates[0] - 60, top_coordinates[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                self.grep_ball = top_most_common_label
            

            # 아래쪽 구역의 객체 정보 출력
            for obj_key, obj_info in self.bottom_objects_data.items():
                bottom_most_common_label, _ = obj_info["labels"].most_common(1)[0]  # 가장 많이 나온 라벨
                bottom_coordinates = obj_info["coordinates"]
                roi_area, roi_idx = self.check_point_in_rois(bottom_coordinates[0],bottom_coordinates[1],ROI, bottom_most_common_label )
                if roi_area is None:
                    continue
                self.cheked_bottom_balls[ROI[roi_idx]["area"]] = bottom_most_common_label
                cv2.putText(self.frame, f"{roi_area}: {bottom_most_common_label}", (bottom_coordinates[0] - 60, bottom_coordinates[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.imshow("YOLOv8 Real-time Detection", self.frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # print("hz :" ,1/(time.time()-start))

    def is_near_existing_object(self, new_center, existing_objects, distance_threshold):
        """기존 객체들과 새로운 객체가 가까운지 확인하여 중복을 방지하는 함수"""
        for obj_info in existing_objects.values():
            existing_center = obj_info["coordinates"]
            if existing_center is not None:
                dist = math.sqrt((new_center[0] - existing_center[0])**2 + (new_center[1] - existing_center[1])**2)
                if dist < distance_threshold:
                    return True
        return False
    
    def check_point_in_rois(self, x, y, rois, bottom_most_common_label):
        for idx, roi  in enumerate(rois):
            if roi["x1"] <= x <= roi["x2"] and roi["y1"] <= y <= roi["y2"]:
                return roi["name"], idx
        
        return None , None
    
    def get_frame(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

    def get_balls_target(self, print_target = True):
        if None in self.cheked_bottom_balls:
            return None
        
        target_list = []
        for ball in self.cheked_bottom_balls:
            target_list.append(ball)

        if print_target:
            print(target_list)

        return target_list
    
    def get_grep_ball_target(self, print_grep_ball = True):
        if self.grep_ball is None:
            return None
        
        if print_grep_ball:
            print(self.grep_ball)

        return self.grep_ball