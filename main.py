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


def ultraDist(i):
    res = ultrasonic2.get(index=i)
    if(res <= 3): return 200
    return res

@event.is_press("b") # triangle button
def followLine():
    KD = 10
    KP = 50
    SPEED = 80
    POS = 0
    PreviousPOS = 0
    PreviousError = 0
    while ultraDist(1)>10:
        lineStatus = quad_rgb_sensor.get_line_sta(index=1)
        s1 = 0 if (lineStatus & (1 << 3)) == 0 else 1
        s2 = 0 if (lineStatus & (1 << 2)) == 0 else 1
        s3 = 0 if (lineStatus & (1 << 1)) == 0 else 1
        s4 = 0 if (lineStatus & (1 << 0)) == 0 else 1
        if(not s1 and not s2 and not s3 and not s4):
            move(85,85)
            continue
        suma = s1 + s2*3 + s3*5 + s4*7
        pesos = s1 + s2 + s3 + s4
        if(pesos > 0):
            POS = suma/pesos
            PreviousPOS = POS
        else:
            POS = PreviousPOS
        error = POS-4
        P = KP*error
        D = KD * (error-PreviousError) 
        move(SPEED + P + D, SPEED - P + D)
        PreviousError=error
    
    mbot2.EM_stop()
    audio.play("beeps")


@event.is_press("left")
def left():
    move(80,80)
    sleep(1)
    move(50,-50)
    sleep(1)
    stop()