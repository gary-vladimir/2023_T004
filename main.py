from cyberpi import *
from time import sleep

LineFollower = 2
BlackMax = 25
ReflectiveMinGreen = 50

def move(left, right):
    mbot2.drive_power(left*-1, right)

def stop():
    mbot2.EM_stop(port="all")

def clasificador(angle):
    mbot2.servo_set(angle, "s1")
    sleep(0.6)

def compuerta(angle):
    mbot2.servo_set(angle, "s2")
    sleep(0.6)

def claw(angle):
    mbot2.servo_set(angle, "s3")
    sleep(0.8)

def closeClaw():
    claw(140)
    
def openClaw():
    claw(70)
        
def elevateClaw(time = 1.2):
    mbot2.motor_set(100, "m2")
    sleep(time)
    mbot2.motor_set(0, "m2")

def lowerClaw(time = 1.2):
    mbot2.motor_set(-100, "m2")
    sleep(time)
    mbot2.motor_set(0, "m2")


def ultraDist(i):
    res = ultrasonic2.get(index=i)
    if(res <= 4): return 200
    return res

def quadRead(i):
    quad_rgb_sensor.set_led(color = "green", index = i)
    s1 = quad_rgb_sensor.get_light("L2", index = i)
    s2 = quad_rgb_sensor.get_light("L1", index = i)
    s3 = quad_rgb_sensor.get_light("R1", index = i)
    s4 = quad_rgb_sensor.get_light("R2", index = i)
    color = ""
    if(s1 > ReflectiveMinGreen and s2 > ReflectiveMinGreen and s3 > ReflectiveMinGreen and s4 > ReflectiveMinGreen): 
        color = "white"

    s1 = 1 if s1 < BlackMax else 0
    s2 = 1 if s2 < BlackMax else 0
    s3 = 1 if s3 < BlackMax else 0
    s4 = 1 if s4 < BlackMax else 0
    return [s1, s2, s3, s4, color]

@event.start
def init():
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=1)
    ultrasonic2.led_show([80,80,80,80,80,80,80,80], index=2)
    quad_rgb_sensor.set_led(color = "green", index = LineFollower)
    clasificador(90)
    compuerta(90)
    led.on(255,255,255)
    console.print("start up successful")
    led.on(50,50,50)

def botella():
    stop()
    led.on(255,0,0)
    move(-60,-60)
    sleep(0.4)
    stop()
    move(60,-60)
    sleep(1.2)
    stop()
    end = True
    while end:
        s3 = quad_rgb_sensor.get_light("R1", index = LineFollower)
        if(s3 < BlackMax): break
        move(50,50)
        second = 0
        while second < 0.4:
            sleep(0.1)
            second += 0.1
            s3 = quad_rgb_sensor.get_light("R1", index = LineFollower)
            if(s3 < BlackMax):
                end = False
                break
        stop()
        move(0,80)
        second = 0
        while second < 0.6:
            sleep(0.1)
            second += 0.1
            s3 = quad_rgb_sensor.get_light("R1", index = LineFollower)
            if(s3 < BlackMax):
                end = False
                break
        stop()
    stop()
    move(60,60)
    sleep(0.2)
    stop()
    while True:
        s3 = quad_rgb_sensor.get_light("R1", index = LineFollower)
        if(s3 < BlackMax): break
        move(60,-60)
    stop()
    led.on(50,50,50)

def findLine(left, right, ch):
    while quad_rgb_sensor.get_light(ch, index = LineFollower) > BlackMax:
        move(left, right)
    stop()

def intersection(direction):
    # TODO check if it's tilted, if so, it means that it-s not an intersection, but a bump instead.
    stop()
    if is_tiltforward(): # TODO increase sensitivity
        audio.play("beeps")
        move(50,50)
        sleep(0.8)
        stop()
        return
    sleep(0.3)
    #TODO add a retreat until not black very slow move
    move(-50,-50)
    sleep(0.4)
    stop()
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    sleep(0.5)
    s4 = quad_rgb_sensor.get_light("R2", index = LineFollower)
    s1 = quad_rgb_sensor.get_light("L2", index = LineFollower)
    s4 = s4 < 50 and s4 > 10
    s1 = s1 < 50 and s1 > 10
    sleep(0.3)
    quad_rgb_sensor.set_led(color = "green", index = LineFollower)
    if s1 and s4:
        led.on("green",0)
        move(80,-80)
        sleep(0.8)
        findLine(60,-60, "r1")
    elif s1:
        led.on("green", id=5)
        move(80,80)
        sleep(0.8)
        move(-80,0)
        sleep(0.5)
        findLine(-50,50, "r1")
    elif s4:
        led.on("green", id=1)
        move(80,80)
        sleep(0.8)
        move(0,-80)
        sleep(0.5)
        findLine(50,-50, "l1")
    elif direction == "left":
        led.on("yellow", id=5)
        move(80,80)
        sleep(0.4)
        findLine(-50,50, "r1")
    elif direction == "right":
        led.on("yellow", id=1)
        move(80,80)
        sleep(0.4)
        findLine(50,-50, "l1")
    led.on(50,50,50)
    
def followLine():
    previousStatus = 1
    status = 1 # 1 = plano, 2 = subida, 3 = bajada
    KD = 15
    KP = 30
    SPEED = 80
    POS = 0
    PreviousPOS = 0
    PreviousError = 0
    while True:
        [s1, s2, s3, s4, color] = quadRead(LineFollower)
        if color == "white": # reflective tape
            break
        # TODO if it's tilted forward, lower the claw all the way, and make the ultrasonic stop
        # TODO if it's tilted back, lower the claw a little
        if(is_tiltforward()):
            status = 2
        elif(is_tiltback()):
            status = 3
        else:
            status = 1
        
        if ultraDist(1) <= 8 and status == 1:
            botella()
        if(not s1 and not s2 and not s3 and not s4):
            move(50,50)
            continue
        
        if(status == 2 and previousStatus == 1):
            stop()
            lowerClaw(0.6)
        elif(status == 3 and previousStatus == 1):
            stop()
            lowerClaw()
        elif(status == 1 and previousStatus == 2):
            stop()
            elevateClaw(0.6)
        elif(status == 1 and previousStatus == 3):
            stop()
            elevateClaw()
            
        if(s1 and s2):
            intersection("left")
        elif(s3 and s4):
            intersection("right")
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
        previousStatus = status
    
    # TODO change led to blue and read again to make sure its a reflective tape, if not. use recursion to continue
    mbot2.EM_stop()
    led.on("cyan")
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    sleep(0.4)
    s1 = quad_rgb_sensor.get_light("L2", index = LineFollower)
    s4 = quad_rgb_sensor.get_light("R2", index = LineFollower)
    if not (s1 > 85 or s4 > 85):
        quad_rgb_sensor.set_led(color = "green", index = LineFollower)
        led.on(50,50,50)
        move(60,60)
        sleep(0.3)
        stop()
        followLine()
    else:
        quad_rgb_sensor.set_led(color = "green", index = LineFollower)
        led.on("white")
        audio.play("beeps")    

@event.is_press("a")
def actionA():
    s1 = quad_rgb_sensor.get_light("L2", index=LineFollower)
    s2 = quad_rgb_sensor.get_light("L1", index=LineFollower)
    s3 = quad_rgb_sensor.get_light("R1", index=LineFollower)
    s4 = quad_rgb_sensor.get_light("R2", index=LineFollower)
    sleep(0.4)
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    sleep(0.4)
    s11 = quad_rgb_sensor.get_light("L2", index=LineFollower)
    s12 = quad_rgb_sensor.get_light("L1", index=LineFollower)
    s13 = quad_rgb_sensor.get_light("R1", index=LineFollower)
    s14 = quad_rgb_sensor.get_light("R2", index=LineFollower)
    string = "\ng: {0},{1},{2},{3}\nb: {4},{5},{6},{7}".format(s1,s2,s3,s4,s11,s12,s13,s14)
    console.print(string)

@event.is_press("b") # triangle button
def actionB():
    followLine()

@event.is_press("right")
def right():
    openClaw()

@event.is_press("left")
def left():
    closeClaw()

@event.is_press("up")
def up():
    elevateClaw()

@event.is_press("down")
def down():
    lowerClaw()
