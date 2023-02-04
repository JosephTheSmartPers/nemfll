from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering
#? Minden osztály beimportálása.


ballMotor = LargeMotor("outB")
jobbMotor = LargeMotor("outC")
tankMotor = MoveTank("outB", "outC")
szogMotor = MoveSteering("outB", "outC")
gs = GyroSensor("in2")
jobbSzenzor = ColorSensor("in3")
ballSzenzor = ColorSensor("in4")
ballSzenzor.MODE_COL_REFLECT = "COL-REFLECT"
jobbSzenzor.MODE_COL_REFLECT = "COL-REFLECT"
#? Szenzorok, és motorok inicializálása

def fordulatszamAtlag():
    return (ballMotor.rotations + jobbMotor.rotations) / 2
#* Megszerzi a két motor fordulatszámának átlagát.    

def kiszamitSzog(fenyKoncentraltsag, joFeny, KP, maxSebesseg):
        sebesseg = (joFeny-fenyKoncentraltsag) * -KP
        #* Kiszámolja a sebességet ami egy helyen egy szög is, a "fenyKoncentraltasag" az valamelyik fény szenzor 
        #* jelenleg olvasott értéke, a "joFeny" pedig a célérték fény koncentráltság szempontjából

        if(abs(sebesseg) > maxSebesseg): sebesseg = maxSebesseg * (sebesseg / abs(sebesseg))
        #? Ha magasabb a megengedett maximumnál a kiszámolt szám, akkor a maximum érték lesz, ezt megszorozzuk egy "házi előjel függvény" eredményével

        return sebesseg     
        #* Visszaadjuk a kiszámolt sebességet, hogy el tudja indítani vele a motort, a vonalKovet eljárás

def vonalKovet(KP, tavolsag, maxSebesseg, joFeny, szenzor = False, egyenes = False):
        tankMotor.on(20,20)
        #? Elindítja a motorokat lassan, hogy meg tudja találni a vonalat

        while egyenes == True:
            if(ballSzenzor.reflected_light_intensity < 10 or jobbSzenzor.reflected_light_intensity < 10):
                break
        tankMotor.stop()
        #* Ha be van kapcsolva a vonalkeresés a paraméterben akkor addig megy amíg egy vonalat nem talál és utána leállítja

        tavolsag += fordulatszamAtlag()
        #? Ne a 0-hoz képest nézze a megtett távolságot

        while tavolsag > fordulatszamAtlag():
        #* Addig megy a ciklus amíg a két motor fordulatszámának az átlaga el nem éri a megadott számot

            if(szenzor != False):
                #? Ez az egy szenzoros vonalkövetés, ami a fentebb látható kiszamitSzog eljárás segítségével számolja ki szöget amiben menni fog
                szogMotor.on(kiszamitSzog(szenzor.reflected_light_intensity, joFeny, KP, maxSebesseg), maxSebesseg)

            else:
                #? Ha a szenzor paraméterben nem adsz meg semmit, vagy hamisat adsz meg, akkor két szenzort használ a vonalkövetésre

                ballMotor.on(maxSebesseg-kiszamitSzog(ballSzenzor.reflected_light_intensity, joFeny, KP, maxSebesseg))
                jobbMotor.on(maxSebesseg-kiszamitSzog(jobbSzenzor.reflected_light_intensity, joFeny, KP, maxSebesseg))
                #? Elindítja a két motort azon a sebességen amit kiszámított 
                #? jobb motort a jobb szenzorral ball motort a ball szenzorral számolja ki
        tankMotor.stop() 

##print(followLine(0.5, 2.9, 25, 40, False, True))

