from cyberpi import *
from time import sleep

LineFollower = 2
BlackMax = 20 # this should be less than the min green value
ReflectiveMinGreen = 50 # mid white value for green fill light
ReflectiveMinBlue = 90 # min reflective value
GreenMax = 55
orientation = "h"
clawUp = 1

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
        
def elevateClaw(time = 1.6):
    mbot2.motor_set(100, "m2")
    mbot2.motor_set(-100, "m1")
    sleep(time)
    mbot2.motor_set(0, "m2")
    mbot2.motor_set(0, "m1")

def lowerClaw(time = 1.3):
    mbot2.motor_set(-100, "m2")
    mbot2.motor_set(100, "m1")
    sleep(time)
    mbot2.motor_set(0, "m2")
    mbot2.motor_set(0, "m1")


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

def subida():
    return get_pitch() <= -15

def bajada():
    return get_pitch() >= 15

@event.start
def init():
    ultrasonic2.led_show([50,50,50,50,50,50,50,50], index=1)
    ultrasonic2.led_show([50,50,50,50,50,50,50,50], index=2)
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
    stop()
    if subida():
        move(50,50)
        sleep(1.2)
        stop()
        return
    sleep(0.2)
    move(-40,-40)
    sleep(0.2)
    stop()
    while True:
        s4 = quad_rgb_sensor.get_light("R2", index = LineFollower) > BlackMax
        s1 = quad_rgb_sensor.get_light("L2", index = LineFollower) > BlackMax
        if direction == "l" and s1:
            stop()
            break
        if direction == "r" and s4:
            stop()
            break
        move(-25,-25)
    move(-40,-40)
    sleep(0.1)
    stop()
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    sleep(0.5)
    s4 = quad_rgb_sensor.get_light("R2", index = LineFollower) <= GreenMax
    s1 = quad_rgb_sensor.get_light("L2", index = LineFollower) <= GreenMax
    sleep(0.3)
    quad_rgb_sensor.set_led(color = "green", index = LineFollower)
    if s1 and s4:
        led.on("green",0)
        move(80,-80)
        sleep(1)
        findLine(60,-60, "r1")
    elif s1:
        led.on("green", id=5)
        move(80,80)
        sleep(0.35)
        move(-80,80)
        sleep(0.3)
        findLine(-50,50, "r1")
    elif s4:
        led.on("green", id=1)
        move(80,80)
        sleep(0.35)
        move(80,-80)
        sleep(0.3)
        findLine(50,-50, "l1")
    elif direction == "l":
        led.on("yellow", id=5)
        move(80,80)
        sleep(0.35)
        findLine(-50,50, "r1")
    elif direction == "r":
        led.on("yellow", id=1)
        move(80,80)
        sleep(0.35)
        findLine(50,-50, "l1")
    led.on(50,50,50)

def handleRamps(status):
    global clawUp
    if status == 2 and clawUp == 1:
        lowerClaw(0.6)
        clawUp = 2
    elif status == 3 and clawUp == 1:
        lowerClaw()
        clawUp = 3
    elif status == 1 and clawUp == 2:
        elevateClaw(0.7)
        clawUp = 1
    elif status == 1 and clawUp == 3:
        elevateClaw()
        clawUp = 1

def getStatus():
    if subida():
        status = 2
    elif bajada():
        status = 3
    else:
        status = 1
    return status

def followLine():
    KD = 1
    KP = 80
    SPEED = 100
    POS = 0
    PreviousPOS = 0
    PreviousError = 0
    while True:
        [s1, s2, s3, s4, color] = quadRead(LineFollower) # s1,s2,s3,s4 are binary. 1 is black, 0 is white
        if color == "white": # posible reflective tape
            break
        status = getStatus()
        if ultraDist(1) <= 8 and clawUp == 1:
            botella()
        if(not s1 and not s2 and not s3 and not s4):
            move(50,50)
            continue
        handleRamps(status)
        if(s1 and s2):
            intersection("l")
        elif(s3 and s4):
            intersection("r")
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
        if status == 3:move((SPEED + P + D)*0.25, (SPEED - P + D)*0.25)
        else: move((SPEED + P + D)*0.4, (SPEED - P + D)*0.4)
        PreviousError=error
    
    # TODO change led to blue and read again to make sure its a reflective tape, if not. use recursion to continue
    stop()
    led.on("cyan")
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    sleep(0.4)
    move(-60,-60)
    sleep(0.2)
    move(30,30)
    continueFollowing = False
    while True:
        status = getStatus()
        handleRamps(status)
        s1 = quad_rgb_sensor.get_light("L2", index = LineFollower)
        s2 = quad_rgb_sensor.get_light("L1", index = LineFollower)
        s3 = quad_rgb_sensor.get_light("R1", index = LineFollower)
        s4 = quad_rgb_sensor.get_light("R2", index = LineFollower)
        if(s1 < BlackMax or s2 < BlackMax or s3 < BlackMax or s4 < BlackMax):
            continueFollowing = True
            break
        if(s2 > ReflectiveMinBlue and s3 > ReflectiveMinBlue):
            break
        
    stop()
    if continueFollowing:
        quad_rgb_sensor.set_led(color = "green", index = LineFollower)
        sleep(0.4)
        followLine()
    audio.play("beeps")

def grabBall():
    stop()
    closeClaw()
    elevateClaw()
    lowerClaw(0.3)
    openClaw()
    lowerClaw(0.3)
    closeClaw()
    lowerClaw(0.7)
    openClaw()
    if quad_rgb_sensor.is_color(color = "black", ch="l1", index=1): clasificador(120)
    else: clasificador(60)
    clasificador(90)

def moveSearchUltras(time, left=60, right=60, considerObstacle=False):
    move(left, right)
    second = 0
    while second < time:
        if considerObstacle and ultraDist(1) <= 15 and ultraDist(2) <= 18:
            return second
        if ultraDist(2) <= 8 and not ultraDist(1) <= 10:
            grabBall()
            move(left, right)
        second += 0.1
        sleep(0.1)
    stop()
    return -1
    
def turn(angle):
    reset_yaw()
    if(angle > 0):move(50,-50)
    else: move(-50,50)
    while True:
        z = get_yaw()
        z *= -1
        if(angle >= 0 and z >= angle):break
        if(angle < 0 and z <= angle):break
    stop()
    if angle > 0: move(-50,50)
    else: move(50,-50)
    sleep(0.1)
    stop()

def findEdge():
    move(60, 60)
    while True:
        if ultraDist(1) <= 15 and ultraDist(2) <= 17:
            break
        if quad_rgb_sensor.get_light("L1", index=LineFollower) < BlackMax:
            stop()
            move(-60,-60)
            sleep(2)
            break
        if ultraDist(2) <= 8 and not ultraDist(1) <= 10:
            grabBall()
            move(60,60)
    stop()
    
def greenTriangle():
    return dual_rgb_sensor.get_green(ch = 1, index = 1) > 25 and dual_rgb_sensor.get_red(ch = 1, index = 1) < 20

def redTriangle():
    return (dual_rgb_sensor.get_red(ch = 1, index = 1) - dual_rgb_sensor.get_green(ch = 1, index = 1)) > 50

def checkCorner():
    moveSearchUltras(2)
    turn(-90)
    turn(-90)
    move(-60,-60)
    sleep(1.3)
    stop()
    green = greenTriangle()
    red = redTriangle()
    if green or red:
        audio.play("beeps")
        if green: led.on("green")
        else: led.on("red")
        move(-60,-60)
        sleep(0.8)
        stop()
        move(55,55)
        sleep(0.35)
        stop()
        if green: compuerta(0)
        else: compuerta(180)
        sleep(1)
        compuerta(90)
        move(-50,-50)
        sleep(0.7)
        stop()
        move(50,0)
        sleep(0.1)
        stop()
    moveSearchUltras(3.7)

distancesVertical = [3,4,3,2,3,4,3]

def collectBalls():
    quad_rgb_sensor.set_led(color = "blue", index = LineFollower)
    lowerClaw()
    openClaw()
    if orientation == "h":
        moveSearchUltras(4.5)
    else:
        moveSearchUltras(6)
    turn(95)
    findEdge()
    move(-60,-60)
    if orientation == "h":
        sleep(4)
    else:
        sleep(2.5)
    stop()
    sleep(5)
    # at this point the robot is in the center and pointing to the long side
    if orientation == "h":
        turn(45)
    else:
        turn(-45)
        
    for dist in distancesVertical:
        time = moveSearchUltras(dist, considerObstacle=True)
        move(-60,-60)
        if time == -1: sleep(dist)
        else: sleep(time)
        stop()
        turn(-45)

def depositBalls():
    turn(-90)
    moveSearchUltras(1.5)
    turn(45)
    checkCorner()
    turn(100)
    checkCorner()
    turn(45)
    moveSearchUltras(2)
    turn(45)
    checkCorner()
    turn(100)
    checkCorner()
    turn(45)
    move(60,60)
    sleep(1.5)
    stop()
    
def moveSearchExit():
    move(60, 60)
    second = 0
    while True:
        if quad_rgb_sensor.get_light("L2", index=LineFollower) < BlackMax or quad_rgb_sensor.get_light("L1", index=LineFollower) < BlackMax or quad_rgb_sensor.get_light("R1", index=LineFollower) < BlackMax or quad_rgb_sensor.get_light("R2", index=LineFollower) < BlackMax:
            stop()
            return True
        if (ultraDist(1) <= 15 and ultraDist(2) <= 17) or quad_rgb_sensor.get_light("L1", index=LineFollower) > ReflectiveMinBlue:
            stop()
            move(-60,-60)
            sleep(second)
            stop()
            return False
        second += 0.18
        
def tryToExit():
    closeClaw()
    elevateClaw()
    global clawUp
    clawUp = 1
    for i in range(4):
        found = moveSearchExit()
        if found: break
        turn(90)
    audio.play("beeps")
    followLine()
    
@event.is_press("a") # square button
def actionA():
    #depositBalls()
    #tryToExit()
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


@event.is_press("middle")
def actionCenter():
    global orientation
    orientation = "v"
    audio.play("beeps")
    g = dual_rgb_sensor.get_green(ch = 1, index = 1)
    r = dual_rgb_sensor.get_red(ch = 1, index = 1)
    debugColorSensor = "\ng:{}\nr:{}".format(g, r)
    console.print(debugColorSensor)
    
@event.is_press("b") # triangle button
def actionB():
    followLine()
    collectBalls()
    sleep(5)
    depositBalls()
    sleep(2)
    tryToExit()


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
