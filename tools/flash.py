import serial
import time
import sys
import os

# Use command-line argument for target file, default to src/main.py
target_file = sys.argv[1] if len(sys.argv) > 1 else "src/main.py"

if not os.path.exists(target_file):
    print(f"Error: Target file '{target_file}' not found.")
    sys.exit(1)

print(f"Reading local file: {target_file}...")
with open(target_file, 'r', encoding='utf-8') as f:
    code = f.read()

PORT = '/dev/cu.usbmodem14102'
BAUDRATE = 115200

print(f"Connecting to {PORT}...")
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=2)
    
    # 1. Stop any running loops with multiple Ctrl+Cs
    print("Stopping micro:bit execution...")
    ser.write(b'\x03')
    time.sleep(0.3)
    ser.write(b'\x03')
    time.sleep(0.3)
    ser.reset_input_buffer()
    
    # Clean prompt
    ser.write(b'\r\n')
    time.sleep(0.2)
    boot_info = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
    print("REPL Prompt Active. Boot Info:")
    print(boot_info)
    
    # Remove existing main.py to prevent any locking/leftover issues
    print("Removing old main.py...")
    ser.write(b"import os; os.remove('main.py')\r\n")
    time.sleep(0.3)
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
    
    # Open fresh file
    print("Creating fresh main.py...")
    ser.write(b"f = open('main.py', 'w')\r\n")
    time.sleep(0.3)
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
    
    # Write line by line with verification
    lines = code.split('\n')
    print(f"Writing {len(lines)} lines...")
    for idx, line in enumerate(lines):
        escaped_line = line.replace("'", "\\'")
        cmd = f"f.write('{escaped_line}\\n')\r\n"
        ser.write(cmd.encode('utf-8'))
        
        # Wait for execution and prompt
        buffer = ""
        t0 = time.time()
        while time.time() - t0 < 1.0:
            if ser.in_waiting > 0:
                buffer += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                if ">>>" in buffer:
                    break
            time.sleep(0.01)
            
        if "Traceback" in buffer or "SyntaxError" in buffer:
            print(f"CRITICAL ERROR at Line {idx+1}: {line}")
            print(buffer)
            ser.close()
            sys.exit(1)
            
        if idx % 20 == 0:
            print(f" -> Successfully wrote {idx}/{len(lines)} lines...")
            
    # Close file
    print("Saving file...")
    ser.write(b"f.close()\r\n")
    time.sleep(0.3)
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
    
    # Soft reset
    print("Performing soft reset (Ctrl+D)...")
    ser.write(b'\x04')
    time.sleep(0.5)
    
    # Print boot messages of the newly running script
    print("Newly booted program output:")
    time.sleep(2.0)
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
    
    ser.close()
    print("Bypass flash completed successfully!")
except Exception as e:
    print("Error:", e)
