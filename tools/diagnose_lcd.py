from microbit import *

display.off()
sleep(200)

i2c.init(freq=100000, sda=pin20, scl=pin19)
sleep(200)

print("=== I2C LCD DIAGNOSTIC ===")
print("Scanning I2C bus...")
found = []
for addr in range(0x08, 0x78):
    try:
        i2c.read(addr, 1)
        found.append(addr)
        print("Found device at 0x{:02X}".format(addr))
    except:
        pass

if not found:
    print("ERROR: No I2C devices found! Check wiring.")
else:
    print("Scan complete. Found:", len(found), "device(s)")

# Try to force backlight ON by writing directly to 0x27
print("")
print("Forcing LCD backlight ON/OFF toggle...")
try:
    for i in range(5):
        print("Blinking backlight...")
        i2c.write(0x27, bytes([0x08]))  # Backlight ON
        sleep(500)
        i2c.write(0x27, bytes([0x00]))  # Backlight OFF
        sleep(500)
    i2c.write(0x27, bytes([0x08]))  # Leave backlight ON
    print("Diagnostic toggle done - did the backlight blink?")
    print("If it blinked but you saw no letters, turn the blue contrast potentiometer on the back of the LCD module.")
except Exception as e:
    print("LCD write failed:", str(e))
