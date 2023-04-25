from cyberpi import *
from time import sleep

LineFollower = 2
BlackMax = 95
ReflectiveMinGreen = 240
GreenMax = 140
orientation = "h"

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
    mbot2.motor_set(-100, "m2")
    mbot2.motor_set(100, "m1")
    sleep(time)
    mbot2.motor_set(0, "m2")
    mbot2.motor_set(0, "m1")

def lowerClaw(time = 1.3):
    mbot2.motor_set(100, "m2")
    mbot2.motor_set(-100, "m1")
    sleep(time)
    mbot2.motor_set(0, "m2")
    mbot2.motor_set(0, "m1")


def ultraDist(i):
    res = ultrasonic2.get(index=i)
    treshold = 4
    if i == 1: treshold = 6
    if(res <= treshold): return 200
    return res

def quadRead(i):
    s1 = quad_rgb_sensor.get_green("L2", index = i)
    s2 = quad_rgb_sensor.get_green("L1", index = i)
    s3 = quad_rgb_sensor.get_green("R1", index = i)
    s4 = quad_rgb_sensor.get_green("R2", index = i)
    color = ""
    if s1 >= ReflectiveMinGreen and s2 >= ReflectiveMinGreen: 
        color = "white"

    s1 = 1 if s1 < BlackMax else 0
    s2 = 1 if s2 < BlackMax else 0
    s3 = 1 if s3 < BlackMax else 0
    s4 = 1 if s4 < BlackMax else 0
    return [s1, s2, s3, s4, color]

def alineacion(left, right):
    while True:
        s1 = quad_rgb_sensor.get_green("L2", index = LineFollower) <= BlackMax
        s4 = quad_rgb_sensor.get_green("R2", index = LineFollower) <= BlackMax
        if s1 and s4:
            break
        m1 = left
        m2 = right
        if s1: m1 = 0
        if s4: m2 = 0
        move(m1, m2)
    stop()
    
@event.start
def init():
    ultrasonic2.led_show([50,50,50,50,50,50,50,50], index=1)
    ultrasonic2.led_show([50,50,50,50,50,50,50,50], index=2)
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
        s3 = quad_rgb_sensor.get_green("L2", index = LineFollower)
        if(s3 < BlackMax): break
        move(42,42)
        second = 0
        while second < 0.8:
            sleep(0.1)
            second += 0.1
            s3 = quad_rgb_sensor.get_green("L2", index = LineFollower)
            if(s3 < BlackMax):
                end = False
                break
        stop()
        move(0,55)
        second = 0
        while second < 1.2:
            sleep(0.1)
            second += 0.1
            s3 = quad_rgb_sensor.get_green("L2", index = LineFollower)
            if(s3 < BlackMax):
                end = False
                break
        stop()
    stop()
    move(0,-75)
    sleep(0.6)
    stop()
    while quad_rgb_sensor.get_green("R2", index = LineFollower) > BlackMax:
        move(0,40)
    move(50,75)
    sleep(0.3)
    alineacion(-30,-30)
    move(60,60)
    sleep(0.9)
    stop()
    move(0,60)
    sleep(1.1)
    stop()
    move(-60,-60)
    sleep(1.3)
    stop()
    findLine(50,-50, "l1")

def findLine(left, right, ch):
    while quad_rgb_sensor.get_green(ch, index = LineFollower) > BlackMax:
        move(left, right)
    stop()

def intersection(direction):
    stop()
    if get_pitch() <= -5:
        move(50,50)
        sleep(1.2)
        stop()
        return
    sleep(0.2)
    move(-40,-40)
    sleep(0.2)
    stop()
    while True:
        s4 = quad_rgb_sensor.get_green("R2", index = LineFollower) > BlackMax
        s1 = quad_rgb_sensor.get_green("L2", index = LineFollower) > BlackMax
        if direction == "l" and s1:
            stop()
            break
        if direction == "r" and s4:
            stop()
            break
        move(-35,-35)
    move(-40,-40)
    sleep(0.1)
    stop()
    s4 = quad_rgb_sensor.get_blue("R2", index = LineFollower) <= GreenMax
    s1 = quad_rgb_sensor.get_blue("L2", index = LineFollower) <= GreenMax
    sleep(0.3)
    if s1 and s4:
        led.on("green",0)
        move(80,-80)
        sleep(1)
        findLine(60,-60, "r1")
    elif s1:
        led.on("green", id=5)
        move(80,80)
        sleep(0.4)
        move(-80,80)
        sleep(0.4)
        findLine(-50,50, "r1")
    elif s4:
        led.on("green", id=1)
        move(80,80)
        sleep(0.4)
        move(80,-80)
        sleep(0.4)
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

def handleRamps(status, claw):
    newClaw = claw
    if status == 2 and claw == 1:
        newClaw = 2
        stop()
        lowerClaw(0.6)
    elif status == 3 and claw == 1:
        newClaw = 3
        stop()
        lowerClaw(1)
    elif status == 1 and claw == 2:
        newClaw = 1
        stop()
        elevateClaw(0.7)
    elif status == 1 and claw == 3:
        newClaw = 1
        stop()
        elevateClaw()
    return newClaw

def getStatus():
    angle = get_pitch()
    if angle <= -15:
        status = 2
    elif angle >= 15:
        status = 3
    elif angle >= -3 and angle <= 3:
        status = 1
    else: status = 4
    return status

def followLine():
    clawStatus = 1
    while True:
        [s1, s2, s3, s4, color] = quadRead(LineFollower) # s1,s2,s3,s4 are binary. 1 is black, 0 is white
        status = getStatus()
        if color == "white" and status == 1: # reflective tape
            break
        if ultraDist(1) <= 8 and ultraDist(2) <= 11 and clawStatus == 1 and status == 1:
            botella()
        if(not s1 and not s2 and not s3 and not s4):
            move(50,50)
            continue
        clawStatus = handleRamps(status, clawStatus)
        if(s1 and s2):
            intersection("l")
        elif(s3 and s4):
            intersection("r")
        elif s2 and s3:
            move(50, 50)
        elif s2:
            move(0,40)
        elif s3:
            move(40,0)
        elif s1:
            move(-75, 30)
        elif s4:
            move(30,-75)

    stop()
    led.on("cyan")
    audio.play("beeps")

def grabBall():
    stop()
    closeClaw()
    elevateClaw()
    lowerClaw(0.2)
    openClaw()
    lowerClaw(0.35)
    closeClaw()
    lowerClaw(0.7)
    openClaw()
    if quad_rgb_sensor.is_color(color = "black", ch="l1", index=1): clasificador(120)
    else: clasificador(60)
    clasificador(90)

def moveSearchUltras(time, left=60, right=60, considerObstacle=False):
    reset_yaw()
    move(left, right)
    second = 0
    while second < time:
        if considerObstacle and ultraDist(1) <= 15 and ultraDist(2) <= 18:
            stop()
            return second
        if ultraDist(2) <= 8 and not ultraDist(1) <= 10:
            grabBall()
            move(left, right)
        if get_yaw()*-1 > 0: move(left, right+10)
        elif get_yaw()*-1 < 0: move(left+5, right)
        else: move(left, right)
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

def findEdge():
    reset_yaw()
    if ultraDist(1) <= 15 and ultraDist(2) <= 17: 
        move(-60,-65)
        sleep(0.7)
        stop()
        return False
    lowerClaw()
    openClaw()
    move(60, 60)
    while True:
        if ultraDist(1) <= 15 and ultraDist(2) <= 17:
            break
        if quad_rgb_sensor.get_green("L1", index=LineFollower) < BlackMax:
            stop()
            move(-60,-65)
            sleep(1.5)
            break
        if ultraDist(2) <= 8 and not ultraDist(1) <= 10:
            grabBall()
            move(60,60)
        angle = get_yaw()*-1
        if angle > 0: move(60,68)
        elif angle < 0: move(64,60)
        else: move(60,60)
    stop()
    return True
    
def greenTriangle():
    return dual_rgb_sensor.get_green(ch = 1, index = 1) > 25 and dual_rgb_sensor.get_red(ch = 1, index = 1) < 20

def redTriangle():
    return (dual_rgb_sensor.get_red(ch = 1, index = 1) - dual_rgb_sensor.get_green(ch = 1, index = 1)) > 50

def checkCorner():
    moveSearchUltras(2)
    turn(-90)
    turn(-90)
    move(-60,-65)
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
        move(75,75)
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

distancesVertical = [3,4.2,3.2,2.6,3.2,4,3]

def collectBalls():
    lowerClaw()
    openClaw()
    if orientation == "h":
        moveSearchUltras(4.5)
    else:
        moveSearchUltras(5.9)
    closeClaw()
    elevateClaw()
    turn(88)
    found = findEdge()
    move(-60,-65)
    if orientation == "h":
        sleep(4.1)
    else:
        sleep(2.5)
    stop()
    if not found:
        lowerClaw()
        openClaw()
    sleep(1)
    # at this point the robot is in the center and pointing to the long side
    if orientation == "h":
        turn(45)
    else:
        turn(-45)

    for dist in distancesVertical:
        time = moveSearchUltras(dist, considerObstacle=True)
        move(-60,-65)
        if time == -1: sleep(dist)
        else: sleep(time)
        sleep(0.4)
        stop()
        turn(-46)

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
        if quad_rgb_sensor.get_green("L2", index=LineFollower) < BlackMax or quad_rgb_sensor.get_green("L1", index=LineFollower) < BlackMax or quad_rgb_sensor.get_green("R1", index=LineFollower) < BlackMax or quad_rgb_sensor.get_green("R2", index=LineFollower) < BlackMax:
            stop()
            return True
        angle = get_pitch()
        if (ultraDist(1) <= 15 and ultraDist(2) <= 17) or (quad_rgb_sensor.get_green("L1", index=LineFollower) >= ReflectiveMinGreen and angle >= -3 and angle <= 3):
            stop()
            move(-60,-65)
            sleep(second)
            stop()
            return False
        second += 0.18
        
def tryToExit():
    closeClaw()
    elevateClaw()
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
    s1 = quad_rgb_sensor.get_green("L2", index=LineFollower)
    s2 = quad_rgb_sensor.get_green("L1", index=LineFollower)
    s3 = quad_rgb_sensor.get_green("R1", index=LineFollower)
    s4 = quad_rgb_sensor.get_green("R2", index=LineFollower)
    sleep(0.4)
    s11 = quad_rgb_sensor.get_blue("L2", index=LineFollower)
    s12 = quad_rgb_sensor.get_blue("L1", index=LineFollower)
    s13 = quad_rgb_sensor.get_blue("R1", index=LineFollower)
    s14 = quad_rgb_sensor.get_blue("R2", index=LineFollower)
    string = "\ng: {0},{1},{2},{3}\nb: {4},{5},{6},{7}\n pitch:{8}".format(s1,s2,s3,s4,s11,s12,s13,s14, get_pitch())
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
