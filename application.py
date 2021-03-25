from djitellopy import Tello
import tkinter as tk
import threading
import cv2
import PIL
from dronevision import DroneVideoCapture
from drone import new_drone
from keys import init, getkeyinp

# define application space
class App:
    
    def __init__(self, window, title, drone: Tello):
        self.window = window
        self.window.title = title
        self.drone = drone
        self.video = DroneVideoCapture(self.drone)
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        self.delay = 15
        self.update_video()
        init()
        self.drive_thread = threading.Thread(target=self.keyboard_control)
        self.drive_thread.start()
        self.window.mainloop()

    def update_video(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def keyboard_control(self):
        while True:
            inp = getkeyinp()
            self.drone.send_rc_control(inp[0], inp[1], inp[2], inp[3])

drone = new_drone()
App(tk.Tk(), 'Tello Drone Controller', drone)
