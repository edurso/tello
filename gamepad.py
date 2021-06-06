from __future__ import print_function
from inputs import get_gamepad
from application import App

def joystick_control_loop(app: App):
    fwd_rev = 0
    left_right = 0
    up_down = 0
    rot = 0
    while app.run:
        events = get_gamepad()
        for event in events:
            if not event.ev_type == 'Sync':
                print('EVENT: {} | {} | {}'.format(event.ev_type, event.code, event.state))
                if event.code == 'ABS_Y':
                    fwd_rev = scale_js(event.state)
                if event.code == 'ABS_X':
                    left_right = scale_js(event.state)
                if event.code == 'ABS_RY':
                    up_down = scale_js(event.state)
                if event.code == 'ABS_RX':
                    rot = scale_js(event.state)
                if event.code == 'BTN_START':
                    if event.state == 1:
                        app.fly = not app.fly
                        if app.fly:
                            app.drone.takeoff()
                        else:
                            app.drone.land()
                if event.code == 'BTN_TR' and event.state == 1:
                    app.drone.flip_right()
                if event.code == 'BTN_TL' and event.state == 1:
                    app.drone.flip_left()

        if app.fly:            
            app.drone.send_rc_control(left_right, fwd_rev, up_down, rot)

def scale_js(val):
    max = 100
    min = 0
    sign = -1 if val < 0 else 1
    val = abs(val) % ( max - min + 1) + min
    return val * sign
