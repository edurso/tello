import threading 
import socket

# https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf

class Drone():

    def __init__(self):
        """
        Initialize Drone Object
        """
        self.local_address = ('',  9001) # (host, port) Local Address
        self.drone_address = ('192.168.10.1', 8889) # (host, port) Tello Address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket
        self.sock.bind(self.local_address) # Bind UDP Transmission to Local Address
        recvThread = threading.Thread(target=self.recv)
        recvThread.start()
        self.command_mode()

    def recv(self):
        """
        Recieves Data From Tello
        """
        while True: 
            try:
                data, server = self.sock.recvfrom(1518)
                print(data.decode(encoding="utf-8")) # TODO write to file
            except Exception:
                print ('\nExit . . .\n')
                break
    
    def send_packet(self, msg: str) -> int:
        """
        Sends the given message to the drone.
        """
        return self.sock.sendto(msg.encode(encoding="utf-8"), self.drone_address)
    
    def interactive_loop_cli(self):
        print ('####################### TELLO DRONE APPLICATION #######################')
        commands = ['command', 'takeoff', 'land', 'flip', 'forward', 'back', 'left', 'right', 'up', 'down', 'cw', 'ccw', 'speed', 'end', 'kill']
        print ('Commands are:\n\t' + '\n\t'.join(commands))
        while True: 
            try:
                msg = input('')
                if not msg:
                    break  
                if 'end' in msg or 'kill' in msg:
                    self.kill() 
                    break
                self.send_packet(msg)
            except KeyboardInterrupt:
                print ('\n . . .\n')
                self.kill() 
                break
    
    def command_mode(self):
        """
        Enables the drone in command mode
        """
        self.send_packet('command')
    
    def takeoff(self):
        """
        Starts autonomous take off sequence
        """
        self.send_packet('takeoff')
    
    def land(self):
        """
        Starts autonomous landing sequence
        """
        self.send_packet('land')

    def set_video(self, on: bool):
        """
        Sets the state of the drone camera to on if True, off otherwise
        """
        self.send_packet('streamon' if on else 'streamoff')

    def estop(self):
        """
        Turn off all motors and close connection
        """
        self.send_packet('emergency')
        self.kill()

    def kill(self):
        """
        Close connection to drone
        """
        self.sock.close()
    
    def left(self, distance: int):
        """
        moves left distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('left ' + str(distance))
    
    def right(self, distance: int):
        """
        moves right distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('right ' + str(distance))
    
    def up(self, distance: int):
        """
        moves up distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('up ' + str(distance))
    
    def down(self, distance: int):
        """
        moves down distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('down ' + str(distance))

    def flip(self, direction: str):
        """
        Filps the drone midair
        accepts either 'f' for forward, 'b' for backward, 'r' for right, or 'l' for left
        """
        if direction == 'f' or direction == 'b' or direction == 'r' or direction == 'l':
            self.send_packet('flip ' + direction)
    
    def forward(self, distance: int):
        """
        moves forward distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('forward ' + str(distance))
    
    def back(self, distance: int):
        """
        moves back distance cm
        distance must be between 20 and 500 cm
        """
        if distance <= 500 and distance >= 20:
            self.send_packet('back ' + str(distance))
    
    def clockwise(self, degrees: int):
        """
        turns clockwise the given degree amount
        the given degree amount must be in between 1 and 3600
        """
        if degrees <= 3600 and degrees >= 1:
            self.send_packet('cw ' + str(degrees))
    
    def counterclockwise(self, degrees: int):
        """
        turns clockwise the given degree amount
        the given degree amount must be in between 1 and 3600
        """
        if degrees <= 3600 and degrees >= 1:
            self.send_packet('ccw ' + str(degrees))

    def set_speed(self, speed: int):
        """
        sets the speed at which the drone travels in cm/s
        must be between 10 and 100 cm/s
        """
        if speed <= 100 and speed >= 10:
            self.send_packet('speed ' + str(speed))
    
    def goto(self, x: int, y: int, z: int, speed: int):
        """
        goes to the given position in the x, y, z, planes with the given speed
        x, y, z must be between 20 and 500 cm
        speed must be between 10 and 100 cm/s 
        """
        if x <= 500 and x >= 20 and y <= 500 and y >= 20 and z <= 500 and z >= 20:
            if speed <= 100 and speed >= 10:
                self.send_packet('go {} {} {} {}'.format(x, y, z, speed))

