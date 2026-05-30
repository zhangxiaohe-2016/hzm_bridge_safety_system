from microbit import *

display.off()
sleep(200)

i2c.init(freq=100000, sda=pin20, scl=pin19)
sleep(500)

print("=== LCD WRITE TEST ===")

# PCF8574 I2C LCD driver
ADDR = 0x27
BL = 0x08  # backlight bit

def pulse(val):
    i2c.write(ADDR, bytes([val | 0x04 | BL]))
    sleep(2)
    i2c.write(ADDR, bytes([val & ~0x04 | BL]))
    sleep(2)

def send(val, mode):
    pulse((val & 0xF0) | mode)
    pulse(((val << 4) & 0xF0) | mode)

def cmd(c):
    send(c, 0)

def char(c):
    send(c, 1)

def write_str(s):
    for c in s:
        char(ord(c))

# Extra long init with generous delays
print("Init step 1...")
sleep(100)
pulse(0x30); sleep(10)
pulse(0x30); sleep(10)
pulse(0x30); sleep(10)
pulse(0x20); sleep(10)   # 4-bit mode

print("Init step 2...")
cmd(0x28); sleep(5)   # 2 lines, 5x7
cmd(0x08); sleep(5)   # display OFF
cmd(0x01); sleep(10)  # clear
cmd(0x06); sleep(5)   # entry mode
cmd(0x0C); sleep(5)   # display ON

print("Writing text...")
cmd(0x80)             # row 0, col 0
write_str("HELLO WORLD!    ")
cmd(0xC0)             # row 1, col 0
write_str("LCD TEST OK     ")

print("Done! Check your LCD screen.")
