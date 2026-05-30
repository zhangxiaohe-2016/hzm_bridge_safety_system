from microbit import *

display.off()
sleep(1000)  # Long wait for LCD to fully power up

i2c.init(freq=100000, sda=pin20, scl=pin19)
sleep(500)

print("=== LCD HARD RESET TEST ===")

ADDR = 0x27
BL = 0x08

def raw(val):
    """Send raw byte to PCF8574"""
    i2c.write(ADDR, bytes([val]))

def pulse_enable(val):
    """Toggle enable pin with backlight always on"""
    raw(val | BL | 0x04)  # E=1
    sleep(2)
    raw(val | BL & ~0x04 & 0xFF)  # E=0
    sleep(2)

def write4(nibble, rs):
    """Send 4-bit nibble. rs=0 for command, rs=1 for data"""
    val = (nibble & 0xF0) | rs | BL
    pulse_enable(val)

def send_byte(byte, rs):
    write4(byte & 0xF0, rs)
    write4((byte << 4) & 0xF0, rs)
    sleep(2)

def cmd(c):
    send_byte(c, 0)

def data(c):
    send_byte(c, 1)

# --- HD44780 Power-On Reset Sequence (from datasheet) ---
print("Step 1: Power-on wait (40ms)...")
sleep(100)

# Send 0x30 three times in 8-bit mode to force reset
print("Step 2: 8-bit mode force...")
raw(0x30 | BL | 0x04); sleep(1); raw(0x30 | BL); sleep(10)
raw(0x30 | BL | 0x04); sleep(1); raw(0x30 | BL); sleep(5)
raw(0x30 | BL | 0x04); sleep(1); raw(0x30 | BL); sleep(2)

# Switch to 4-bit mode
print("Step 3: Switch to 4-bit...")
raw(0x20 | BL | 0x04); sleep(1); raw(0x20 | BL); sleep(10)

# Now in 4-bit mode - configure
print("Step 4: Configure...")
cmd(0x28); sleep(2)   # 4-bit, 2 lines, 5x8 font
cmd(0x08); sleep(2)   # Display OFF
cmd(0x01); sleep(5)   # Clear display
cmd(0x06); sleep(2)   # Entry mode: increment, no shift
cmd(0x0C); sleep(2)   # Display ON, cursor OFF, blink OFF

print("Step 5: Writing text...")
cmd(0x80)  # Set DDRAM addr = 0 (row 0, col 0)
sleep(1)
for ch in "HELLO WORLD!    ":
    data(ord(ch))
    sleep(1)

cmd(0xC0)  # Set DDRAM addr = 0x40 (row 1, col 0)
sleep(1)
for ch in "LCD HARD RESET  ":
    data(ord(ch))
    sleep(1)

print("Done! Any text on screen?")
