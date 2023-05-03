#3rd place in robocup rescue line junior 2023
this was our first time participating in this competition and we managed to obtain the highest individual round score using a pure Makeblock line follower solution

!["el inge"](robot.jpg)

## Lessons learned
### 1. Make sure to read the rules properly to have a good strategy
in the last week before the competition we realized that the evacuation zone part took too much time and it didn't give out any points. they were multiplicators instead. if we had known this earlier we should have adjusted our strategy to only focus on a save algorithm for following line

### 2. Consider all edge cases
we didn't test many obstacles over line cases because we thought they were unlikely due to their difficulty. However, they were present on the track and they were passable with some adjustments to the code that involved the gyro sensor.

### 3. get_status() > getlight().
significant improvement in read speed for the line follower and because you can calibrate using the build button by putting the sensor over the green tape and then to the line there is no need to read the light intensity.

### 4. Keep it simple
in many rounds, the line follower sensor failed to detect an intersection and the ultrasonic object. this is likely due to having too many unnecessary electronics making the motherboard freeze.

### 5. check ultrasonic readings
we realized that sometimes the ultrasonic sensor would read 0 when there is absolutely no object in front. We fixed this problem by having an ultraDist() function that checks for reading greater than 3 cm

### 6. Create FULL 3d assembly
Make sure to always model everything, especially the electronics, we managed to avoid many failed 3d prints thanks to the simulation.

### 7. Measurements
for a Lego hole, 5.2 mm, for a make block hole 4.3 mm, separation from hole to hole 8 mm.

### 8. Safety is Priority
for the next year make sure to not change the chassis since passing the speed bumps is a high priority

### 9. Consider smaller balls for the next year
in this TMR competition 2023 the balls were way smaller, they looked about the size of a ping pong ball.

### 10. Detect the reflective Tape
this was one of the biggest problems this year, first, we had a light-intensity approach, but it was very common for false positives to happen, which were absolutely not wanted and sometimes the sensor failed to detect the tape at all. We ended up using a timer approach, where we checked if the sensor was on a white gap for more than 6 seconds. but there was a big problem with this approach on the real round, and that was that the reflective tape was exactly in the middle of a tile and the zone, making a 5 mm slope that was detected as an intersection. we made a partial fix that worked but only when the robot was entering the reflective tape completely straight, (in the fourth round there was a curve for entering the rescue zone)

for the next year think of a different solution, maybe adding an IR light sensor for that unique purpose. 