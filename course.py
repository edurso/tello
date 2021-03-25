from tello import Drone
from time import sleep

drone = Drone()

drone.takeoff()
sleep(5)
drone.goto(100, 100, 100, 100)
sleep(5)
drone.estop()

drone.kill()