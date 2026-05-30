from microbit import *

display.off()
sleep(200)

i2c.init(freq=100000, sda=pin20, scl=pin19)
sleep(200)

print("Scanning I2C bus on P20 (SDA) and P19 (SCL)...")
found = []
for addr in range(0x08, 0x78):
    try:
        i2c.read(addr, 1)
        found.append(addr)
        print("Found active device at address: 0x{:02X}".format(addr))
    except:
        pass

if not found:
    print("No I2C devices found. Check your connections, power, and SCL/SDA pins.")
else:
    print("Scan complete. Found", len(found), "devices.")
