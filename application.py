from djitellopy import Tello
import tkinter as tk
import threading
import cv2
import PIL
import gamepad as gp
from dronevision import DroneVideoCapture
from drone import new_drone

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
        gp.joystick_control_loop(self)

    def __del__(self):
        return

drone = new_drone()
App(tk.Tk(), 'Tello Drone Controller', drone)
