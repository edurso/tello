from tello import Drone
from time import sleep

drone = Drone()

drone.takeoff()
sleep(5)
drone.clockwise(90)
sleep(3)
drone.forward(100)
sleep(5)
drone.land()

drone.kill()