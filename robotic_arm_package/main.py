from robotic_arm import RoboticArm
from camera_detection import CameraDetection

def main():

    c = CameraDetection(1,'model')
    c.start()

    return 0
    
if __name__ == '__main__':
    main()