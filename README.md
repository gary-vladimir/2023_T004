# 3th place in robocup rescue line junior 2023
this was our first time participating in this competition and we managed to obtain the highest individual round score using a pure Makeblock line follower solution

!["el inge"](robot.jpg)

## lessons learned
### 1. make sure to read the rules properly to have a good strategy
in the last week before the competition we realized that the evacuation zone part took too much time and it didn't give out any points. they were multiplicators instead. if we had known this earlier we should have adjusted our strategy to only focus on a save algorithm for following line

### 2. Consider all edge cases
we didn't test many obstacle over line cases because we thought they were unlikly due to it's dificulty. However they were present on the track and they were passable with some adjustments to the code that involved the gyro sensor.

### 3. get_status() > getlight().
significant improvment on read speed for the line follower and because you can calibrate using the build in button by putting the sensor over the green tape and then to the line there is no need to read the light intensity.

### 4. Keep it simple
in many rounds the line follower sensor failed to detect an intersection and the ultrasonic the object. this is likly due to having too much unecesary electronics making the motherboard freeze.

