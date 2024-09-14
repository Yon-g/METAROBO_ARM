import cv2

class CameraDetection:
    
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open video device")
            exit()

    def __del__(self):
        self.cap.release()        
        cv2.destroyAllWindows()

    def detection(self):
        ret, frame = self.cap.read()

        