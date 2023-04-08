from cyberpi import *
from time import sleep

def move(left, right):
    mbot2.drive_power(left*-1, right)

def stop():
    mbot2.EM_stop(port="all")

@event.start
def init():
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=1)
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=2)
    led.on(255,255,255)
    console.print("start up successful")
    led.on(50,50,50)
    
@event.is_press("left")
def left():
    move(80,80)
    sleep(1)
    move(50,-50)
    sleep(1)
    stop()