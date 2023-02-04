from ev3dev2.sensor.lego import GyroSensor
from visszaallit import *
from time import sleep
from ev3dev2.motor import MoveTank, MediumMotor
#? Mindent beimportálunk

yKez = MediumMotor("outD")
xKez = MediumMotor("outA")
gs = GyroSensor("in2")
m = MoveTank("outB", "outC")
#? Motorok és szenzorok inicializálása

def kalibral(visszaallitKez = False):
    gs.calibrate()
    m.stop()
    m.reset()
    #* Kalibrálja a giroszkópot és lenullázza a motor értékeit. 

    if(visszaallitKez == True):
        visszaallit(yKez, 2.5)
        visszaallit(xKez, 1.1)
    #* Ha a paraméterben benne van, megrpóbálja alap helyzetbe állítani a két kezet
    
    xKez.reset()
    yKez.reset()
    sleep(0.2)
    #* A két motor értékeit is visszaállítja- 
