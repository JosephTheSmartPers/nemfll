from ev3dev2.motor import MediumMotor
#? Motor osztály betöltése

yKez = MediumMotor("outA")
xKez = MediumMotor("outD")
#? Két motor definiálása

def visszaallit(motor, maxFordulatok):
    motorFordulatok = motor.rotations
    if(abs(motorFordulatok) > maxFordulatok):
        motorFordulatok = (abs(motorFordulatok) / motorFordulatok) * maxFordulatok
        #? Ha túl magas akkor a maxFordulatok változó értékénél nem fordulhat többet

    motor.on_for_rotations(90, motorFordulatok * -0.95 )
    motor.reset()
    #* Elfordítja a motort a kiszámolt értékkel és utána lenulláza a motor méréseit.

#* Ez a funkció alapból megnézii, hogy mennyi a fordulatszáma a motornak, és annyival elforgatja a másik irányba, 
#* viszont van egy határ, ami fölött biztosan lehet tudni, hogy kaparni fog, ott meg fog állni a program.
#* Ezért nem használjuk a "motor.on_to_position()" eljárást, mert ott nincs ilyen határ.
