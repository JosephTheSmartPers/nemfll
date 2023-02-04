from ev3dev2.motor import MoveTank
from ev3dev2.sensor.lego import GyroSensor
import time
#? Mindent beimportálunk

gs = GyroSensor("in2")
m = MoveTank("outB", "outC")
gs.MODE_GYRO_ANG = 'GYRO-ANG'
#? Szenzorok és motorok inicializálása

def fordul(szog, maxSebesseg, gyorsulas, koIdo, hibahatar = 2, idotullepes = 3, relativ = True, motorLe = False):
    kezdoIdo = time.time()
    #? Fordulás kezdetének időpontja

    elozoIdo = 999999999999
    elteltIdo = time.time() - elozoIdo
    #? Now nagy szám, mivel kivonjuk a mostani időből, mivel ezt nézi az egyik programrész

    szog = szog * -1
    #? Így megy a jó irányba, gyro meg van fordítva

    fordulatszam = 0
    if(relativ == True):
        fordulatszam = gs.angle
    #* 0-hoz képest vagy a gyrohoz képest forduljon el adott szögben
    
    while gs.angle != fordulatszam - szog:

        if(kezdoIdo + idotullepes <= time.time()):
            break
        #* Ha túl sokáig csinálja a fordulást akkor abbahagyja, mert lehet, hogy be van akadva

        elteltIdo = time.time() - elozoIdo
        #* Ez egy nagy számmal negatív lesz, ha viszont az előzőidő valóban az előző idő akkor megkapod 
        #* a két számolás közti különbséget, és ezt hozzáadjuk a változóhoz

        if(((fordulatszam - szog) - hibahatar <= gs.angle <= (fordulatszam - szog)  + hibahatar) and elozoIdo > time.time()):
            elozoIdo = time.time()
        #* Ha már közel van a giroszkóp a célértékhez, akkor elkezdi mérni az időt

        if(elteltIdo >= koIdo):
            m.stop()
            break
        #* Ha a robot már közel van a cél szöghöz, akkor lesz még egy adott ideje, hogy kisebbet korigáljon, aztán abbahagyja

        sebesseg = (fordulatszam - szog - gs.angle) * gyorsulas
        #* Kiszámolja a sebességet, ami egyre lassul minnél közelebb vagy a cél giroszkóp értékhez

        if(abs(sebesseg) > abs(maxSebesseg)): sebesseg = (abs(maxSebesseg) * (abs(sebesseg) / sebesseg))
        #* Ne lépje túl megadott felső sebességkorlátot 

        m.on(sebesseg * -1, sebesseg)
        #* Elindítja a motorokat forduláshoz ellenkező irányokba.
    
    if(motorLe != False):
        m.on(motorLe, motorLe)
    else:
        m.stop()
    
    
    #print("Kész a fordulás, célértéktől való eltérés: " + str(round(float(abs((((gs.angle / szog) * 100) - 100))), 2)) + "%")
    
  
#fordul(50, 70, 0.7, 2)