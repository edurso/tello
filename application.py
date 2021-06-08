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
    
    def __init__(self, window, title, drone: Tello):
        self.window = window
        self.window.title = title
        self.drone = drone
        self.vid = DroneVideoCapture(self.drone)
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.delay = 120

        # Start Video Thread
        # self.update_video()

        # Start Control Thread
        self.joystick_control_loop()

        # Quit Button
        self.btn_snapshot=tk.Button(window, text="Quit", width=50, command=self.toggle_running)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # Run Loop in Main Thread
        #self.window.mainloop()

    def update_video(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update_video)

    def toggle_running(self):
        self.run = not self.run

    def joystick_control_loop(self):
        fwd_rev = 0
        left_right = 0
        up_down = 0
        rot = 0
        run = True
        fly = False
        while run:
            events = get_gamepad()
            for event in events:
                if not event.ev_type == 'Sync':
                    #print('EVENT: {} | {} | {}'.format(event.ev_type, event.code, event.state))
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
                    if event.code == 'BTN_TR' and event.state == 1:
                        self.drone.flip_right()
                    if event.code == 'BTN_TL' and event.state == 1:
                        self.drone.flip_left()

            if fly:            
                self.drone.send_rc_control(left_right, fwd_rev, up_down, rot)

    def scale_js(self, val):
        inputRange = 32768 - (-32767)
        outputRange = 100 - (-100)
        val = int((val - (-32767)) * outputRange / inputRange + (-100))
        return val if abs(val) > 30 else 0

    def __del__(self):
        return

drone = new_drone()
App(tk.Tk(), 'Tello Drone Controller', drone)
