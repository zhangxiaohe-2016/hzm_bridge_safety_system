from microbit import *
import neopixel

display.off()
sleep(200)

print("=== NEOPIXEL STRIP TEST ===")
print("Testing 12 RGB LEDs on P16 with safe power currents (low brightness)...")

np = neopixel.NeoPixel(pin16, 12)

while True:
    print("Color: Safe Warm Amber (8, 8, 4)")
    for i in range(12):
        np[i] = (8, 8, 4)
    np.show()
    sleep(1500)
    
    print("Color: Safe Green (0, 8, 0)")
    for i in range(12):
        np[i] = (0, 8, 0)
    np.show()
    sleep(1500)

    print("Color: Safe Red (8, 0, 0)")
    for i in range(12):
        np[i] = (8, 0, 0)
    np.show()
    sleep(1500)
    
    print("Color: OFF")
    np.clear()
    np.show()
    sleep(1500)
