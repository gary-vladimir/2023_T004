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
    quad_rgb_sensor.set_led(color = "b", index = 1)
    led.on(255,255,255)
    console.print("start up successful")
    led.on(50,50,50)


def ultraDist(i):
    res = ultrasonic2.get(index=i)
    if(res <= 4): return 200
    return res

def quadRead(i):
    quad_rgb_sensor.set_led(color = "b", index = 1)
    s1 = quad_rgb_sensor.get_light("L2", index = i)
    s2 = quad_rgb_sensor.get_light("L1", index = i)
    s3 = quad_rgb_sensor.get_light("R1", index = i)
    s4 = quad_rgb_sensor.get_light("R2", index = i)
    color = ""
    if(s2 > 75 and s3 > 75): 
        color = "white"
    
    s1 = 1 if s1 < 40 else 0
    s2 = 1 if s2 < 40 else 0
    s3 = 1 if s3 < 40 else 0
    s4 = 1 if s4 < 40 else 0
    return [s1, s2, s3, s4, color]

@event.is_press("b") # triangle button
def followLine():
    KD = 10
    KP = 45
    SPEED = 100
    POS = 0
    PreviousPOS = 0
    PreviousError = 0
    while True:
        [s1, s2, s3, s4, color] = quadRead(1)
        if color == "white": # reflective tape
            break

        if(not s1 and not s2 and not s3 and not s4):
            move(50,50)
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
        if(is_tiltback()):move((SPEED + P + D)*0.35, (SPEED - P + D)*0.35)
        else: move((SPEED + P + D)*0.65, (SPEED - P + D)*0.65)
        PreviousError=error
    
    mbot2.EM_stop()
    audio.play("beeps")

@event.is_press("right")
def test():
    [s1, s2, s3, s4, color] = quadRead(1)
    debug = "{0},{1},{2},{3},{4}\n".format(s1,s2,s3,s4,color)
    console.print(debug)

@event.is_press("left")
def left():
    move(80,80)
    sleep(1)
    move(50,-50)
    sleep(1)
    stop()