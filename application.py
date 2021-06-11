from time import sleep
from djitellopy import Tello
import tkinter as tk
import threading
import cv2
import PIL
import PIL.Image, PIL.ImageTk
from dronevision import DroneVideoCapture
from drone import new_drone
from inputs import get_gamepad

# define application space
class App:
    
    def __init__(self, drone: Tello):
        self.drone = drone
        threading.Thread(target=lambda: self.video(drone)).start()
        self.run = True

        # Start Control Loop
        self.joystick_control_loop()


    def video(self, drone: Tello):
        self.vid = DroneVideoCapture(drone)
        ret, frame = self.vid.get_frame()
        while ret and self.run:
            cv2.imshow('Tello Drone Control', frame)  
            if cv2.waitKey(25) & 0xFF == ord('q'):
                self.run = False
                break
            #sleep(50)  

    def joystick_control_loop(self):
        fwd_rev = 0
        left_right = 0
        up_down = 0
        rot = 0
        fly = False
        while self.run:
            events = get_gamepad()
            for event in events:
                if not event.ev_type == 'Sync':
                    if event.code == 'ABS_Y':
                        fwd_rev = self.scale_js(int(event.state))
                    if event.code == 'ABS_X':
                        left_right = self.scale_js(int(event.state))
                    if event.code == 'ABS_RY':
                        up_down = self.scale_js(int(event.state))
                    if event.code == 'ABS_RX':
                        rot = self.scale_js(int(event.state))
                    if event.code == 'BTN_START':
                        if event.state == 1:
                            fly = not fly
                            if fly:
                                self.drone.takeoff()
                            else:
                                self.drone.land()
                                self.run = False
                    if event.code == 'BTN_TR' and event.state == 1 and fly:
                        self.drone.flip_right()
                    if event.code == 'BTN_TL' and event.state == 1 and fly:
                        self.drone.flip_left()
            if fly:            
                self.drone.send_rc_control(left_right, fwd_rev, up_down, rot)
            
            #sleep(20)

    def scale_js(self, val):
        inputRange = 32768 - (-32767)
        outputRange = 100 - (-100)
        val = int((val - (-32767)) * outputRange / inputRange + (-100))
        return val if abs(val) > 30 else 0

    def __del__(self):
        return

App(new_drone())
