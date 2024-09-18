import cv2
import threading
from ultralytics import YOLO
import numpy as np
import math
from collections import defaultdict, Counter

# Load the YOLOv8 trained model

MARGIN = 10
DISTANCE_THRESHOLD = 20

class CameraDetection:
    def __init__(self, camera_serial_number = 0, model_path = None):
        print("Init CameraDetection")
        print("Camera Loading")
        self.cap = cv2.VideoCapture(camera_serial_number)
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

    def __del__(self):
        print("Destroy CameraDetection")
    
    def start(self):
        print("starta thread")
        threading.Thread(target=self.update, args=()).start()
        return self
    
    def detection_ball(self, result, height, width, center_y):
        boxes = result.boxes.xyxy.numpy()  # 객체탐지 박스 경계좌표(왼쪽위, 오른아래쪽)
        confidences = result.boxes.conf.numpy()  # 정확도
        class_ids = result.boxes.cls.numpy()  # 클래스 라벨값

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            conf = confidences[i]
            if conf >= 0.30:  # 정확도 30% 이상인지 확인
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

        while not self.stopped:

            self.ret, self.frame = self.cap.read()
            
            # 프레임 정보 확인
            height, width = self.frame.shape[:2]

            # (화면을 위아래로 나누기 위한 중앙선 설정)
            center_y = height // 2

            results = self.model.predict(self.frame, verbose=False)

            for result in results:
                self.detection_ball(result, height, width, center_y)

            if count%100 == 0:
                # 위쪽 구역의 객체 정보 출력
                print("Top Region:")
                for obj_key, obj_info in self.top_objects_data.items():
                    most_common_label, _ = obj_info["labels"].most_common(1)[0]  # 가장 많이 나온 라벨
                    coordinates = obj_info["coordinates"]
                    print(f"Coordinates: {coordinates}, Most common label: {most_common_label}")

                # 아래쪽 구역의 객체 정보 출력
                print("Bottom Region:")
                for obj_key, obj_info in self.bottom_objects_data.items():
                    most_common_label, _ = obj_info["labels"].most_common(1)[0]  # 가장 많이 나온 라벨
                    coordinates = obj_info["coordinates"]
                    print(f"Coordinates: {coordinates}, Most common label: {most_common_label}")
            
    def is_near_existing_object(new_center, existing_objects, distance_threshold):
        """기존 객체들과 새로운 객체가 가까운지 확인하여 중복을 방지하는 함수"""
        for obj_info in existing_objects.values():
            existing_center = obj_info["coordinates"]
            if existing_center is not None:
                dist = math.sqrt((new_center[0] - existing_center[0])**2 + (new_center[1] - existing_center[1])**2)
                if dist < distance_threshold:
                    return True
        return False

    def get_frame(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()