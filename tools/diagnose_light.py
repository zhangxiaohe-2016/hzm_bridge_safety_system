from microbit import *

display.off()
sleep(200)

print("=== LIGHT SENSOR DIAGNOSTIC ===")
print("Cover and uncover the light sensor on P0 to calibrate your daylight/nighttime threshold!")
print("Normal Day (bright): high values (~270)")
print("Normal Night (covered): low values (~73)")
print("Current threshold is set to 150.")
print("")

while True:
    v = pin0.read_analog()
    state = "DAY (bright, LEDs OFF)" if v < 150 else "NIGHT (dark, LEDs ON)"
    print("Analog P0 Read =", v, " => Current State:", state)
    sleep(500)
