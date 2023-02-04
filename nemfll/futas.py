from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, MoveSteering

ballMotor = LargeMotor("outB")
jobbMotor = LargeMotor("outC")
yKez = MediumMotor("outA")
xKez = MediumMotor("outD")

tankMozgas = MoveTank("outB", "outC")
szogMozgas = MoveSteering("outB", "outC")
gs = GyroSensor("in2")
jobbSzenzor = ColorSensor("in3")
ballSzenzor = ColorSensor("in4")

ballSzenzor.MODE_COL_REFLECT = "COL-REFLECT"
jobbSzenzor.MODE_COL_REFLECT = "COL-REFLECT"
gs.MODE_GYRO_ANG = 'GYRO-ANG'

from vonalKovet import *
from fordul import *
from egyenes import *
from visszaallit import *



"""
reset(yhand, 2.5)
reset(xhand, 1.1)
"""
#! Visszaállítja a alap pozicóba a karokat, kaparásveszély

def futas1():

    kezdoIdo = time()

    egyenes(2.67, 60, 3, 1.2, 20)
    xKez.on_for_rotations(90, -1)
    #) Első víz cellához odamegy és mögé viszi a vízszintes kart

    egyenes(1.8, -60, 3, 1.1, 20)
    yKez.on_for_rotations(90, 0.4, False, False)
    #) Hátramegy, és ezáltal a home-ba behozza a kék cellát 

    egyenes(2.1, 60, 3, 1, 20)
    yKez.on_for_rotations(100, 1)
    xKez.on_for_rotations(90, 0.7)
    egyenes(0.2, -20, 0, 1.2, 20)
    #) Odamegy a vízerőműhöz, és a zöld cella fölé viszi a kart, és felemeli, ezáltal kigurl a zöld cella, utána picit hátramegy

    sleep(0.6) 
    #! Megvárjuk, hogy visszaguruljon a zöld a cella

    fordul(51, 47, 0.3, 0.5, relativ=False, motorLe=20)
    #) Ráfordul a dobozra


    xKez.on_for_rotations(-50, 0.8, False, False)
    yKez.on_for_rotations(10, 0.4, False, False)
    egyenes(4, 70, 46, 0.8, 20)
    #) Odamegy dobozhoz, közben elhúzza, mert nekimenne a kútnak a kart.

    yKez.on_for_rotations(45, -1.8)
    #) Leengedi a kart, és a pöcök belemegy a doboz piros részébe

    egyenes(1.25, -30, int(gs.angle), 1.2, 10)
    #) Odamegy olajkút mellé

    raiseSpeed = 100
    raiseHeight = 0.7
    xKez.on_for_rotations(raiseSpeed, 0.45)
    #) a vízszintes kart behúzza az olajkút karja alá


    yKez.on_for_rotations(raiseSpeed, raiseHeight + (1.1 - raiseHeight))
    yKez.on_for_rotations(raiseSpeed, -raiseHeight)
    yKez.on_for_rotations(raiseSpeed, raiseHeight)
    yKez.on_for_rotations(raiseSpeed, -raiseHeight)
    yKez.on_for_rotations(raiseSpeed, raiseHeight)
    yKez.on_for_rotations(raiseSpeed, -raiseHeight)
    yKez.on_for_rotations(raiseSpeed, raiseHeight)
    yKez.on_for_rotations(raiseSpeed, (-1 * (raiseHeight + (1.1 - raiseHeight))))
    xKez.on_for_rotations(-10, 0.5, False, False)
    #) Kiszedi az olajat a kútból

    egyenes(6, -90, int(gs.angle) - 20, 1.5, 20)
    #) Hazajön miközben lefelé viszi karját

    print("Kész az 1. futás " + str(round(float(time() - kezdoIdo), 2)) + "mp alatt")

    visszaallit(xKez, 1.1)
    #) Visszaállítja vertikálisan mozgó kart

    yKez.stop()
    tankMozgas.stop()
    
    yKez.on_for_rotations(40, 1.2)
    #) Felemeli függőleges kart a következő futáshoz

def futas2():
    egyenes(1.7, 80, int(gs.angle) + 2.5, 0.5, 20)
    #) Előre megy a kocsihoz

    m.on_for_rotations(-10, -10, 0.1)
    yKez.stop()
    yKez.on_for_rotations(-100, 0.85, False)
    #) Leengedi a kezet hogy belemenjen a kamion elejébe

    egyenes(3.1, -80, int(gs.angle)+20, 0.5, 20)
    yKez.on_for_rotations(-100, 0.35)
    #) Hátramegy és reseteli a kezet

def futas3(): 
    egyenes(7.6, 45, int(gs.angle)+0.3, 1, 20)
    fordul(-58, 20, 0.7, 1)
    egyenes(2.1, 25, int(gs.angle), 1, 20)
    #) a három kapszula összegyűjtése

    yKez.on_for_rotations(40, 1.6)
    fordul(40, 10, 0.7, 1)
    egyenes(0.12, -30, int(gs.angle), 1, 20)
    fordul(-115, 20, 0.7, 1)
    #) a kéz  behajtása

    egyenes(0.8, -80, int(gs.angle)-20, 1, 20)
    sleep(0.05)
    gs.reset()
    sleep(0.05)
    #) falazás megvan

    egyenes(3.5, 30, gs.angle+19, 0.8, 20)
    egyenes(1, 30, 70, 0.5, 20)
    #) három kapszula körbe helyezése

    yKez.on_for_rotations(-40, 1.6)
    egyenes(1, -30, int(gs.angle)+50, 1, 20)
    fordul(-58, 10, 0.7, 1)
    egyenes(2, 15, int(gs.angle), 1, 10, True, False)
    #) megáll a vonalra az erőmű felé

    fordul(-(gs.angle-10), 20, 0.3, 1)
    yKez.on_for_rotations(40, 0.35)
    egyenes(1.3, 30, 10, 1, 20)
    fordul(-7, 20, 0.5, 1)
    #) beáll az erőműbe

    yKez.on_for_rotations(-40, 0.35)
    egyenes(0.53, 20, 0, 1, 20)
    egyenes(0.25, -10, 0, 1, 10)
    #) Kiszedi a középső cellát

    egyenes(0.2, -10, 0, 1, 10)
    egyenes(0.25, 10, 0, 1, 10)
    #) Hátramegy és előrmegy, mert beleakadhat a pálya magába

    yKez.on_for_rotations(40, 1.5)
    egyenes(0.5, 20, 0, 1, 20)
    egyenes(0.25, -30, 0, 1, 20)
    #) Kiszedte az összes celllát az erőműből

    yKez.on_for_rotations(-40, 1.45)
    egyenes(1, -40, 0, 1, 20, motorLe=-20)
    egyenes(2.2, 80, 75, 1, 20, motorLe=80)
    egyenes(4.8, 80, 90, 1, 20, gyorsuljon=False)
    
    yKez.on_for_rotations(-40, 0.1)
    #) visszamegy a másik home-ba
    m.stop()

def futas4():
    gs.reset()
    startTime = time()
    #? Elmenti a futás kezdetének idejét, így a végén ki lehet számolni, hogy mennyi időbe telt a futás.

    xKez.on_for_rotations(100, 2, True, False)
    #! Fontos, hogy ne mozogjon a tároló a roboton, amit az egyik kar irányít, ezért bekapcsolja a fékeket

    egyenes(2.4, 70, 0, 1.2, 20, motorLe=15)
    egyenes(0.6, 15, 0, 0.8, 15)
    #) Nekimegy a kanapénak, a végén már lassabban

    egyenes(0.5, -60, 0, 1.2, 20)
    #) Hátramegy egy picit, hogy ne menjen neki a kanapénak ha elindul előre

    fordul(45, 40, 0.3, 0.3, relativ=False, hibahatar=5)
    egyenes(4.38, 80, 45, 1, 20)
    #) Ráfordul és odamegy a felfüggesztett kocsihoz

    yKez.on_for_rotations(100, 0.5, True, False)
    #) Felemeli a kart, és ezáltall lerakja a kamiont

    egyenes(0.68, -45, int(gs.angle), 1, 20)
    yKez.on_for_rotations(-100, 0.4, True, False)
    #) Hátramegy és közben leviszi a kart újra, különben nem tudja a rávezetőt használni

    fordul(-45, 28, 0.3, 0.2, relativ=False)
    egyenes(3.2, 70, -43, 1.2, 30)
    
    #) Ráfordul és nekimegy a szélturbina piros pöckének
    sleep(0.1)
    egyenes(0.25, -35, gs.angle, 0.8, 50)
    sleep(0.2)
    egyenes(0.85, 45, gs.angle, 0.9, 35)

    sleep(0.1)
    egyenes(0.25, -35, gs.angle, 1.4, 50)
    sleep(0.2)
    egyenes(0.85, 45, gs.angle, 1.4, 30)
    #) Nekimegy még kétszer, hogy kiszedje mind a három cellát

    sleep(0.2)
    egyenes(0.25, -35, gs.angle, 1.4, 50)
    sleep(0.2)
    egyenes(0.85, 45, gs.angle, 1.4, 30)
    #! Plusz nekimenés a biztonság kedvéért

    yKez.on_for_rotations(-100, 0.1, True, False)
    egyenes(2.4, -45, -50, 1.4, 20, motorLe=-15)
    egyenes(0.6, -15, -50, 1.4, 15)
    #) Nekimegy a piros gyűjtőnek, és belerakja a 3 cellát

    egyenes(0.7, 45, int(gs.angle), 1.4, 20)
    fordul(130, 35, 0.3, 0.4, relativ=False)
    egyenes(0.1, 10, int(gs.angle), 1.4, 10)
    #) Előremegy, egy picit, hogy legyen helye, és megfordul 180 fokban

    xKez.on_for_seconds(-70, 0.8, True)
    sleep(0.3)
    yKez.on_for_rotations(100, 0.4)
    sleep(0.2)
    xKez.on_for_seconds(10, 0.6, True)
    yKez.on_for_rotations(100, 1.8)
    
    #) Előremegy enyhén és kiengedi az energia cellákat

    """
    egyenes(0.3, 10, int(gs.angle), 1.4, 10)
    
    #) Picit nekimegy a celláknak, mivel lehet hogy rajta van a határon, vagy arrafelé gurul
    # """
    egyenes(0.4, -25, int(gs.angle), 1.4, 20)
    egyenes(5, 100, 225, 1.4, 20)
    #) Hazajön a robot

    yKez.on_for_rotations(-100, 0.6, True)
    #) Felemelve hagyja a kart az 5. futáshoz. 

    print("Kész a 4. futás " + str(round(float(time() - startTime), 2)) + "mp alatt")

def futas5():
    startTime = time()
    
    egyenes(6.3, 70, -5, 0.9, 10)
    #) Odamegy a körbe

    yKez.on_for_rotations(100, 0.9, True)
    yKez.on_for_rotations(-15, 0.9, True, False)
    egyenes(3, 70, 0, 1.35, 20)
    #) Felemeli a függőleges kart, és utána nagyon lassan elkedzi leengedni,
    #) viszont el is indul lefelé, ezért otthagyyja az inovációs projektet

    
    yKez.on_for_rotations(-70, 1.41)
    sleep(0.5)
    egyenes(0.8, -70, 0, 1.35, 20)
    #) Belemegy a vízerőműbe, leengedi a kart és a 3 cellát bennehagyja a körben, utána egy picit hátramegy

    egyenes(7, 80, 50, 1.35, 20)
    #) Hazamegy
    
    #print("Kész az 5. futás " + str(round(float(time() - startTime), 2)) + "mp alatt")





"""gs.reset()
while True:
    gyroSensi = float(input("Mi legyen a KP?: "))
    gs.reset()
    gs.calibrate()
    sleep(0.1)
    print(gs.angle)
    egyenes(4, 10, gs.angle, gyroSensi, 10)
    egyenes(4, -10, gs.angle, gyroSensi, 10)
    #1.4"""


