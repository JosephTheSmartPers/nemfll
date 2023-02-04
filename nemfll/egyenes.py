from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
from time import time, sleep
#? Mindent beimportál ami kell, viszont semmi mást mert lassabb lenne

ballMotorKimenet = "outB"
jobbMotorKimenet = "outC"
#? Két motor outputját definiálom, mivel többször is használom, így nem kell midnkét helyen átírnom ha valamiért változna az output.

ballMotor = LargeMotor(ballMotorKimenet)
jobbMotor = LargeMotor(jobbMotorKimenet)
tankMozgas = MoveTank(ballMotorKimenet, jobbMotorKimenet)
szogMozgas = MoveSteering(ballMotorKimenet, jobbMotorKimenet)
#? Motorfajták inicializálása

gs = GyroSensor("in2")
jobbSzenzor = ColorSensor("in3")
ballSzenzor = ColorSensor("in4")
#? Inputok definiálása

def raallSzog(motor, szinSzenzor, minFeny, maxSebesseg, KP):
    sebesseg = (minFeny - szinSzenzor.reflected_light_intensity) * KP
    #& Egyik oldali motor sebességének kiszámolása, egy célérték (minLight) és egy érzékenység (KP) alapján

    if(abs(sebesseg) > maxSebesseg):            
        sebesseg = maxSebesseg * (sebesseg / abs(sebesseg))
    #* Semmiképp se legyen az sebesség magasabb a megadott maximum sebességnél

    motor.on(sebesseg)
    #* Elindítja a motort a kiszámolt sebességgel

    return sebesseg
    #* Visszaadja a sebességet, hogy meg lehesen nézni hogy, 0, és mindkét motornak 0 lett a sebessége, akkor leáll a program.

def fordulatok():
    return ballMotor.rotations + jobbMotor.rotations / 2
#& Függvény, ami lekéri a két motor fordulatának átlagát, ez azért jó mert így sokkal szebb a kód ahol erre szükség lenne.

def raall(KP, maxIdo, maxSebesseg, minimumFeny):
    elozoIdo = time()
    #? Vonalra állás kezdetének időpotját lementi

    while True:            
        elteltIdo = time() - elozoIdo
        #* Fordulás óta eltelt idő

        if(raallSzog(ballMotor, ballSzenzor, minimumFeny, maxSebesseg, KP) == 0 and raallSzog(jobbMotor, jobbSzenzor, minimumFeny, maxSebesseg, KP) == 0):
            tankMozgas.stop(None, False)
            break
        #* Elindítja a motorokat a funkciókkal és megnézi, hogy mindkettő 0
        #* ha igen akkor leállítja a programot, mert elivleg sikeresen ráállt a vonalra

        if(elteltIdo >= maxIdo):
            tankMozgas.stop(None, False)
            break
        #* Ha túlment az időkorláton akkor is leállítja a programot, mivel ennyi idő után, már lehet hogy túl fog korrigállni
        

def egyenes(fordulatSzam, maximumSebesseg, irany, KP, minimumSebesseg, vonalonAll = False, korigal = False, motorLe = False, lassuljon = True, gyorsuljon = True):
    gyorsulas = fordulatSzam * 0.5
    lassulas = fordulatSzam * 0.6
    #? Kiszámollja, hogy meddig kell gyorsulnia, és mitől fogva kell lassulnia,

    pontos = 0
    osszesMeres = 0
    #? Ezekkel majd később meg lehet nézni az egyenesen menés pontosságát

    if(gyorsulas > 1.5):
        gyorsulas = 1.5
    if(lassulas > 1.5):
        lassulas = 1.5
    #* Ne gyorsuljon túl sokáig

    alapFordulatszam = fordulatok()
    #? Kezdeti fordulatszámot lementi, hogy lehessen abszolútértékekkel számolni 
    #? (olyan mintha lenulláznád a fordulatok számát, ha kivonod belőlók ezt a számot)

    deltaIdo = time()
    #? Lementi az egyenesen menés kezdetét

    if(maximumSebesseg < 0):   
        minimumSebesseg = minimumSebesseg * -1
    #? Ne kelljen a programozónak mindkét értéket átírnia negatív előjelűre, mivel az kimondhatattlanul megeröltető

    while abs(fordulatok() - alapFordulatszam) <= fordulatSzam:
        #* Addig megy az eljárás amíg a motor forduatszáma meg nem egyezik a paraméterben megadott fordulatszámmal
        #* Kivonjuk az eljárás kezdetén lemért fordulatszámot, így olyan mintha a kezdeti érték 0 lenne, és az abszlút érték ugyanaz előre és hátra menésnél

        if(vonalonAll == True):
            if(ballSzenzor.reflected_light_intensity <= 7 or jobbSzenzor.reflected_light_intensity <= 7):
                #* Ha be vonalraállás benne van a paraméterekben, és talál egy vonalat akkor megáll
                if(korigal == True):
                    raall(1.75, 1.5, 15, 6)
                    #* Ha ponotsan vonalra állás be van kapcsolva akkor elindítja azt az eljárást.
                tankMozgas.stop(None, False)
                break
                #* Leállítja fékek nélkül a motort
        
        if(abs(fordulatok() - alapFordulatszam) < gyorsulas and gyorsuljon == True):
            #* Ha a kezdet óta a fordulatok száma még kisebb annál a cél-fordulat számnál amit megadtunk, akkor tovább gyorsul
            sebesseg = (abs(fordulatok() - alapFordulatszam) / gyorsulas * (maximumSebesseg - minimumSebesseg)) + minimumSebesseg
            #~   [              0 és 1 közötti szám           ]   maximum elérhető érték (nem számítjuk a minimum sebességet) + alap sebesség

        elif(abs(fordulatok() - alapFordulatszam) > fordulatSzam - lassulas and lassuljon == True):
            if(motorLe != False):
                minimumSebesseg = motorLe
            #* Ha ez be van kapcsolva, akkor csak egy adott sebességig lassul, és utána bekapcsolva hagyja a motort
            sebesseg = maximumSebesseg - ((abs(fordulatok() - alapFordulatszam) - (fordulatSzam - lassulas)) / lassulas * maximumSebesseg) + minimumSebesseg
            #~               [                        1 és 0 közötti szám                      ]    legalacsonyabb sebessége a minimum érték lehet
            
        else:
            sebesseg = maximumSebesseg
        #* Ha nem gyorsul vagy lassul akkor maximum sebességel menjen
        if(abs(sebesseg) > abs(maximumSebesseg)): sebesseg = (abs(sebesseg) / sebesseg) * abs(maximumSebesseg)
        #* Ne tudjon véletlenül sem a maximum sebességnél gyorsabban menni

        szog = ((irany *-1) - (gs.angle * -1)) * KP
        #~     gyro célérték     jelenlegi gyro érték * érzékenység

        if(maximumSebesseg < 0):
            szog = szog * -1
        #* Ne forduljon meg a robot hátra menésnél

        if(abs(szog) > 100): szog = (abs(szog) / szog) * 100
        #* Ne tudjon a maximumnál nagyobb értékkel fordulni

        if(gs.angle == irany):
            pontos += 1
        osszesMeres += 1
        #* Pontosságot számolja

        szogMozgas.on(szog, sebesseg)
        #* Elindítja a motort a kiszámolt sebességel és szögben.

    

    if(motorLe != False):
        tankMozgas.on(motorLe, motorLe)
    else:
        tankMozgas.stop(None, False)
    #* Ha így bekapcsolva marad a 

    if(osszesMeres != 0):
    #* Ha nem állt le azonnal a program írjon statisztikát
        #print("Kész az egyenesen menés")
        print("Kész az egyenesen menés "+ str(round(float(time() - deltaIdo),2)) +" mp alatt"+", pontosság: " + str(int(pontos/osszesMeres * 100)) + "%")
        return
#straight(5, 60, int(gs.angle), 1.4, 20)
#straight(5, -60, int(gs.angle), 1.4, 20)
