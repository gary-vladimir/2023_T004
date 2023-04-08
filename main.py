from cyberpi import *
from time import sleep

@event.start
def init():
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=1)
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=2)
    led.on(255,255,255)
    console.print("start up successful")
    led.on(50,50,50)
    
    