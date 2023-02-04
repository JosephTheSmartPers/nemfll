from ev3dev2.sensor.lego import * 
from ev3dev2.sensor import *
gs = GyroSensor("in2")

gs.calibrate()

while True:
    print(gs.angle)
    time.sleep(1)