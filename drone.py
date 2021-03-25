from djitellopy import Tello

def new_drone() -> Tello:
    drone = Tello()
    drone.connect()
    drone.for_back_velocity = 0
    drone.left_right_velocity = 0
    drone.up_down_velocity = 0
    drone.yaw_velocity = 0
    drone.speed = 0
    drone.streamoff()
    drone.streamon()
    return drone
    