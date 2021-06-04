from djitellopy import Tello
import tkinter as tk
import threading
import cv2
import PIL
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
        self.delay = 15

        # Start Video Thread
        self.vid_thread = threading.Thread(target=self.update_video)
        self.vid_thread.start()

        # Start Control Thread
        self.control_thread = threading.Thread(target=self.joystick_control_loop)
        self.control_thread.start()

        # Quit Button
        self.btn_snapshot=tk.Button(window, text="Quit", width=50, command=self.toggle_running)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
        self.run = True
        self.fly = False

        # Run Loop in Main Thread
        self.window.mainloop()

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
        while self.run:
            events = get_gamepad()
            for event in events:
                if not event.ev_type == 'Sync':
                    print('EVENT: {} | {} | {}'.format(event.ev_type, event.code, event.state))
                    if event.code == 'ABS_Y':
                        fwd_rev = self.scale_js(event.state)
                    if event.code == 'ABS_X':
                        left_right = self.scale_js(event.state)
                    if event.code == 'ABS_RY':
                        up_down = self.scale_js(event.state)
                    if event.code == 'ABS_RX':
                        rot = self.scale_js(event.state)
                    if event.code == 'BTN_START':
                        if event.state == 1:
                            self.fly = not self.fly
                            if self.fly:
                                self.drone.takeoff()
                            else:
                                self.drone.land()
                    if event.code == 'BTN_TR' and event.state == 1:
                        self.drone.flip_right()
                    if event.code == 'BTN_TL' and event.state == 1:
                        self.drone.flip_left()

            if self.fly:            
                self.drone.send_rc_control(left_right, fwd_rev, up_down, rot)

    def scale_js(self, val):
        max = 100
        min = 0
        sign = -1 if val < 0 else 1
        val = abs(val) % ( max - min + 1) + min
        return val * sign

    def __del__(self):
        return

drone = new_drone()
App(tk.Tk(), 'Tello Drone Controller', drone)
