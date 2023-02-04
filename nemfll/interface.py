#!/usr/bin/env micropython
from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.sound import Sound
from kalibral import *
from futas import *
#? Minden szükséges modul beimportálása

hangszoro = Sound()
konzol = Console()
konzol.set_font(font='Lat15-Terminus32x16', reset_console=False)

gs = GyroSensor("in2")
gs.mode = GyroSensor.MODE_GYRO_ANG
gomb = Button()
#? Inicializálja a gombokat, a konzolt, a girót, és a hangszoórót

jelenlegiFutas = "1Futas"
#? Ez az a futás ami éppen ki van választva, ami alapból az egyes.

futas2Ujra = 0
futas5Ujra = 0
#? Ennél a 2 futásnál még az előtte lévő futásban felemeli a kart, ezért ha újra kell indítani akkor rosz helyen lehett,
#?  emiatt azt számoljuk és hogyha már nem elsőre indítjuk el, akkor előtte a 0-hoz képest felemeli annyira a kart amennyire kéne


kalibral()
#* Kalibrálja a giroszkópot, és lenullázza a motorokat


yKez.on_for_rotations(50, 1)
yKez.on_for_rotations(-50, 1)
xKez.on_for_rotations(-50, 1)
xKez.on_for_rotations(50, 1)
#* Megnézi, hogy bármelyik kar kapar e

#* Itt lentebb egy gombal kettő akciót lehet kiválasztani, ezt mind a négy szélső gombal meg lehet csinálni. 
#* Ha egyszer megnyomod akkor az egyik akciót, ha mégegyszer akkor a másik akciót, aztán újra az elsőt választja ki.

def fel(state):
    if state:
        return
    else: 
        if(jelenlegiFutas == "1Futas"):
            kiirFutas("5Futas")  
        else:
            kiirFutas("1Futas")      

def jobbra(state):
    if state:
        return
    else:
        if(jelenlegiFutas == "1Futas"):
            kiirFutas("2Futas")
        else:
            kiirFutas("1Futas") 

def le(state):
    if state:
        return
    else: 
        if(jelenlegiFutas == "3Futas"):
            kiirFutas("4Futas")
        else:
            kiirFutas("3Futas")  

def balra(state):
    if state:
        return
    else:
        if(jelenlegiFutas == "5Futas"):
            kiirFutas("Kalibral")
        else:
            kiirFutas("5Futas")

def enter(state):
    if state:
        return
    else: 
        if(jelenlegiFutas != None):
            elinditFutas()


gomb.on_left = balra
gomb.on_right = jobbra
gomb.on_up = fel
gomb.on_down = le
gomb.on_enter = enter
#? A gombok eseménykezelője

def kiirGiro():
    angle = gs.angle
    leftside = "    "
    if(angle <= -100):
        leftside = "   "
    #* Ez a rész arra ügyel, hogy mindig pontosan középen legyen a kiírt érték

    konzol.text_at("   " +"G: %03d" % (angle) + leftside, column=2, row=1, reset_console=True, inverse=True)
    #? Kiírja a giroszkóp fordulatszámát, hogy látszódjon, hogyha "mászik"

def kiirFutas(futas):
    
    konzol.text_at(futas, column=2, row=3, reset_console=False, inverse=True)
    
    global jelenlegiFutas
    jelenlegiFutas = futas
#? Kiirja a jelenlegi futást, hogy látszódjon melyik van kiválasztva

futE = False

def elinditFutas():
    global futE
    if(futE == True):
        return
    futE = True
    global jelenlegiFutas
    global futas5Ujra
    global futas2Ujra
    if(jelenlegiFutas == "none" or jelenlegiFutas == None):
        return
    #* Megnézi, hogy valóban ki van e választva valami

    gs.reset()
    m.stop()
    sleep(0.1)
    #* Lenullázza a giroszkópot, hogy abszolútértékesen is lehessen számolni, és ne kelljen minden function elején megcsinálni

    if jelenlegiFutas == "Tisztit":
        #tisztit()
        pass
    
    if jelenlegiFutas == "Visszaalit":
        kalibral(True)
    if jelenlegiFutas == "Kalibral":
        kalibral()
    if jelenlegiFutas == "1Futas":
        futas1()
        futas5Ujra = 0
        futas2Ujra = 0
    if jelenlegiFutas == "2Futas":
        if(futas2Ujra != 0 or 760 > yKez.rotations > 700):
            yKez.on_for_rotations(40, 1.2, False, False)
        futas2Ujra += 1
        #* Ennél és az 5-ös futásnál az előző futás felemeli a kart, viszont mivel újrapróbálod, ezt érzékeli és felemeli
        futas2()
        
    if jelenlegiFutas == "3Futas":
        futas3()
    if jelenlegiFutas == "4Futas":
        futas4()
    if jelenlegiFutas == "5Futas":
        print(yKez.rotations)
        if(futas5Ujra != 0):
            
            yKez.on_for_rotations(40, 1.43, False)
            sleep(1.5)
        futas5Ujra += 1
            #* Ugyanúgy mint a kettes futásnál, az előző futás felemeli a kart, viszont mivel újrapróbálod, ezt érzékeli és felemeli
        futas5()
    #* Ezek maguk a futások, és hogyha megnyomod a fölső gombot, akkor megszakítja mindegyiket, ezt "Key Remapping" segítségével érjük el

    if(jelenlegiFutas.replace("Futas", "").isdigit() and jelenlegiFutas.replace("Futas", "") != "5"):
        jelenlegiFutas =  str((int(jelenlegiFutas.replace("Futas", "")) + 1)) + "Futas"
    else:
        jelenlegiFutas = "1Futas"
    #* Ha egy futás van kiválasztva, akkor a következő futást választja ki ami számrendben utána jön automatikusan
    futE = False
    kiirGiro()

elozoGiro = 0
elozoFutas = "none"

hangszoro.play_tone(frequency=400, duration=0.05)
hangszoro.play_tone(frequency=600, duration=0.05)
hangszoro.play_tone(frequency=800, duration=0.05)
hangszoro.play_tone(frequency=1000, duration=0.05)
hangszoro.play_tone(frequency=1200, duration=0.05)
#* Lejátszik egy menő hangot amikor betölt a program

while True:
    try: 
        gomb.process()
        #* A gombokat ellenőrzi

        if(gs.angle != elozoGiro or jelenlegiFutas != elozoFutas):
            #* Hogyha változott a giroszkóp értéke, vagy változott a kiírt futás, akkor ábrázolja
            kiirGiro()
            if(jelenlegiFutas and jelenlegiFutas != "none"):
                konzol.text_at("R: " + jelenlegiFutas, column=2, row=3, reset_console=False, inverse=True)
            elozoGiro = gs.angle
            elozoFutas = jelenlegiFutas
    except KeyboardInterrupt:
        m.stop()
        m.reset()
        futE = False
        gomb.wait_for_released("up", 2000)
        hangszoro.play_tone(frequency=2500, duration=0.50)
        #* Ha a fölső gombot valaki megnyomja akkor megáll a robot.


