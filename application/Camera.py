import cv2

class Camera() :
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def capture_image(self):
        """ 현재 프레임을 캡처하여 저장 """
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("captured_frame.jpg", frame)

    def capture_face(self,cropped_face):
        """ 현재 프레임을 캡처하여 저장 """
        cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
        # if ret:
        cv2.imwrite("captured_frame.jpg", cropped_face)
        # ret, frame = self.cap.read()
        # if ret:
        #     cv2.imwrite("captured_frame_original.jpg", frame)


    def get_frame(self):
        ret, frame = self.cap.read()
        # if ret:
        #     frame = cv2.resize(frame, (640, 480))
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     frame = cv2.flip(frame, 1)
        
        return ret, frame
    
    def close(self):
        if self.cap.isOpened():
            self.cap.release()