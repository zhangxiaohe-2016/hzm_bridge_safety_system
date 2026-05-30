from microbit import *

display.off()
sleep(200)

green = pin12
yellow = pin13
red = pin14

print("=== TRAFFIC LIGHT TEST ===")
print("Toggling Green, Yellow, and Red traffic lights on P12, P13, P14...")

while True:
    print("GREEN ON (P12)")
    green.write_digital(1)
    yellow.write_digital(0)
    red.write_digital(0)
    sleep(1000)
    
    print("YELLOW ON (P13)")
    green.write_digital(0)
    yellow.write_digital(1)
    red.write_digital(0)
    sleep(1000)
    
    print("RED ON (P14)")
    green.write_digital(0)
    yellow.write_digital(0)
    red.write_digital(1)
    sleep(1000)
