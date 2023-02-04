import ev3dev2.motor as ev3
import sys, termios, tty, os

# Connect motors
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')

print("EV3 brick successfully connected to motors")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

while True:
    # Read the keyboard input
    char = getch()

    # Move forward
    if char == 'w':
        motor_left.run_forever(speed_sp=900)
        motor_right.run_forever(speed_sp=900)

    # Turn left
    elif char == 'a':
        motor_left.run_forever(speed_sp=-450)
        motor_right.run_forever(speed_sp=450)

    # Turn right
    elif char == 'd':
        motor_left.run_forever(speed_sp=450)
        motor_right.run_forever(speed_sp=-450)

    # Stop
    elif char == 's':
        motor_left.stop()
        motor_right.stop()

    # Invalid command
    elif char == 'q':
        break

    # Invalid command
    else:
        print("Invalid command")
