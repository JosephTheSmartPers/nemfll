#!/usr/bin/env micropython
from ev3dev2.sensor.lego import GyroSensor 
from ev3dev2.motor import OUTPUT_C, OUTPUT_B, MoveTank, MediumMotor
from ev3dev2.button import Button
gomb = Button()
#? Szükséges dolgok beimportálása

yhand = MediumMotor("outD")
xhand = MediumMotor("outA")
gs = GyroSensor("in2")
m = MoveTank(OUTPUT_B, OUTPUT_C)
#? Minden motor és szenzor inicializálása

gomb.wait_for_released("enter", 2000)
def tisztit():
    m.on(20, 20)
    while True:
        if(gomb.any()):
            m.stop(None, False)
            gomb.wait_for_released(gomb.buttons_pressed, 2000)
            #? Itt azért vár maximum 2 másodpercig, mert ha nem várja meg, hogy elengedd a gombot 
            #? akkor érzékelni fogja az interfész program, és újra elindítaná
            break
#* Addig megy a motor amíg bármelyik motort meg nem nyomod
tisztit()