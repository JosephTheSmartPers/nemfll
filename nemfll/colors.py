from ev3dev2.sensor.lego import * 
from ev3dev2.sensor import *

gs = GyroSensor(INPUT_2)
rs = ColorSensor("in3")
bs = ColorSensor("in4")

bs.MODE_COL_REFLECT = "COL-REFLECT"
rs.MODE_COL_REFLECT = "COL-REFLECT"

while True:
    print("______________________")
    print(" ")
    print("Jobb = " + str(rs.reflected_light_intensity))
    print("Ball = " + str(bs.reflected_light_intensity))
    print(" ")
    time.sleep(1)