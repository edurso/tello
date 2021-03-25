from djitellopy import Tello
import cv2

# define drone video capture 
class DroneVideoCapture:
    def __init__(self, drone: Tello):
        self.vid = drone.get_video_capture()
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) if ret else (ret, None)
        else:
            return (None, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            