import pygame
from djitellopy import Tello

def init():
    pygame.init()
    window = pygame.display.set_mode((400,400))

def getkey(keyname):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyname))

    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

def getkeyinp(drone: Tello):
    lr, fb, ud, yv = 0, 0, 0, 0
    SPEED = 50 # cm/key press
    TURN = 50
    if getkey("LEFT"): lr = -SPEED       
    if getkey("RIGHT"): lr = SPEED       
    if getkey("UP"): fb = SPEED          
    if getkey("DOWN"): fb = -SPEED       
    if getkey("w"): ud = SPEED           
    if getkey("s"): ud = -SPEED          
    if getkey("a"): yv = -TURN           
    if getkey("d"): yv = TURN            
    if getkey("e"): drone.takeoff()      
    if getkey("q"): drone.land()         
    return (lr, fb, ud, yv)
