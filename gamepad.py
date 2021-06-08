from __future__ import print_function
from inputs import get_gamepad

def joystick_control_loop():
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
                    fwd_rev = scale_js(int(event.state))
                if event.code == 'ABS_X':
                    left_right = scale_js(int(event.state))
                if event.code == 'ABS_RY':
                    up_down = scale_js(int(event.state))
                if event.code == 'ABS_RX':
                    rot = scale_js(int(event.state))
                if event.code == 'BTN_START':
                    if event.state == 1:
                        fly = not fly
                        if fly:
                            print('takeoff') # app.drone.takeoff()
                        else:
                            print('land') # app.drone.land()
                if event.code == 'BTN_TR' and event.state == 1:
                    print('flip right') # app.drone.flip_right()
                if event.code == 'BTN_TL' and event.state == 1:
                    print('flip left') # app.drone.flip_left()

        if fly:            
            print('{} {} {} {}'.format(left_right, fwd_rev, up_down, rot)) # app.drone.send_rc_control(left_right, fwd_rev, up_down, rot)

def scale_js(val):
    inputRange = 32768 - (-32767)
    outputRange = 100 - (-100)
    val = int((val - (-32767)) * outputRange / inputRange + (-100))
    return val if abs(val) > 30 else 0

joystick_control_loop()