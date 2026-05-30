from microbit import *
import neopixel
import music

# Compact, self-contained PCF8574 I2C 1602 LCD Driver Class
class I2CLcd1602:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        self.backlight = 0x08  # Bit 3: Backlight control ON
        
        sleep(50)
        self.write_nibble(0x30)
        sleep(5)
        self.write_nibble(0x30)
        sleep(1)
        self.write_nibble(0x30)
        self.write_nibble(0x20) # 4-bit mode
        
        self.write_cmd(0x28)  # 4-bit mode, 2 lines, 5x7 font
        self.write_cmd(0x0C)  # Display ON, Cursor OFF, Blink OFF
        self.write_cmd(0x06)  # Entry mode
        self.clear()

    def write_nibble(self, val):
        self.i2c.write(self.addr, bytes([val | 0x04 | self.backlight]))
        sleep(1)
        self.i2c.write(self.addr, bytes([val & ~0x04 | self.backlight]))
        sleep(1)

    def write_byte(self, val, mode):
        high = (val & 0xF0) | mode
        low = ((val << 4) & 0xF0) | mode
        self.write_nibble(high)
        self.write_nibble(low)

    def write_cmd(self, cmd):
        self.write_byte(cmd, 0)

    def write_data(self, data):
        self.write_byte(data, 1)

    def clear(self):
        self.write_cmd(0x01)
        sleep(2)

    def puts(self, text, x=0, y=0):
        addr = 0x80 + (y * 0x40) + x
        self.write_cmd(addr)
        for char in text:
            self.write_data(ord(char))

# --- HARDWARE CONFIGURATION ---
# 1. Disable the built-in LED matrix display to resolve P3 pin conflicts
display.off()
sleep(500)

print("Starting Hong Kong-Zhuhai-Macao Bridge Smart Safety System...")
i2c.init(freq=100000, sda=pin20, scl=pin19)

# Define hardware pins
green_led = pin12
yellow_led = pin13
red_led = pin14
buzzer = pin15
trig = pin1
echo = pin2

# Initialize Neopixel strip on P16 with exactly 12 pixels!
num_pixels = 12
np = neopixel.NeoPixel(pin16, num_pixels)

# Variables
car_count = 0
car_in_zone = False # High-precision vehicle state lock to prevent duplicate counting

def get_distance():
    try:
        trig.write_digital(0)
        sleep_us(2)
        trig.write_digital(1)
        sleep_us(10)
        trig.write_digital(0)
        
        import machine
        duration = machine.time_pulse_us(echo, 1, 30000)
        
        if duration < 0:
            return 999.0
            
        distance = (duration / 2) / 29.1
        return distance
    except Exception:
        return 999.0

# Initialize LCD
lcd = I2CLcd1602(i2c, addr=0x27)
lcd.puts("HZM BRIDGE SAFE", 0, 0)
lcd.puts("SYSTEM ACTIVE", 1, 1)
sleep(1500)
lcd.clear()

# Main Safety System Loop
while True:
    # --- 1. Read Environmental Sensors ---
    light_val = pin0.read_analog()
    wind_val = pin3.read_analog()
    dist = get_distance()
    
    # --- 2. Vehicle Detection & Anti-Duplicate Counting Logic ---
    if dist < 8.0:
        if not car_in_zone:
            car_count += 1
            car_in_zone = True
            buzzer.write_digital(1)
            sleep(40)
            buzzer.write_digital(0)
    elif dist > 12.0:
        car_in_zone = False

    # --- 3. Light Control Logic ---
    # CONFIRMED by telemetry: uncovered(bright)=LOW(~73), covered(dark)=HIGH(~267)
    # - LOW (<150)  = uncovered = bright = DAY  -> LEDs OFF
    # - HIGH (>=150) = covered  = dark  = NIGHT -> LEDs ON
    if light_val < 150:  # LOW = bright = DAY
        is_day = True
        np.clear()
        np.show()
    else:  # HIGH = dark = NIGHT
        is_day = False
        # High brightness (60, 60, 30) now that robust 12V power supply is connected!
        for i in range(12):
            np[i] = (60, 60, 30)
        np.show()

    # --- 4. Wind Control Logic & Safety Decision-Making ---
    if wind_val <= 400:
        green_led.write_digital(1)
        yellow_led.write_digital(0)
        red_led.write_digital(0)
        buzzer.write_digital(0)
        wind_label = "NORM"
        status_label = "GO  "
    elif 400 < wind_val <= 800:
        green_led.write_digital(0)
        yellow_led.write_digital(1)
        red_led.write_digital(0)
        buzzer.write_digital(0)
        wind_label = "MID "
        status_label = "SLOW"
    else:
        green_led.write_digital(0)
        yellow_led.write_digital(0)
        red_led.write_digital(1)
        buzzer.write_digital(1)
        sleep(100)
        buzzer.write_digital(0)
        wind_label = "STRG"
        status_label = "STOP"

    # --- 5. Dynamic 1602 LCD Dashboard Display ---
    day_label = "DAY  " if is_day else "NIGHT"
    row0_str = "CAR:{:<2}  WIND:{}".format(car_count, wind_label)
    row1_str = "{}  STATUS:{}".format(day_label, status_label)
    
    lcd.puts(row0_str, 0, 0)
    lcd.puts(row1_str, 0, 1)
    
    print("TELEMETRY -> Light:", light_val, "| Wind:", wind_val, "| Dist:", dist, "cm | Cars:", car_count)
    
    sleep(150)
