from ev3dev2.motor import OUTPUT_C, OUTPUT_B, MoveTank, MediumMotor, OUTPUT_A, OUTPUT_D
from visszaallit import *
print("ready")
m = MoveTank(OUTPUT_B, OUTPUT_C)
leftMotorOutput = "outB"
rightMotorOutput = "outC"
m.stop()
m.reset()

"""yhand = MediumMotor(OUTPUT_A)
xhand = MediumMotor(OUTPUT_D)"""
#reset(yhand, 2.5)
#reset(xhand, 1.1)
xKez.reset()
yKez.reset()