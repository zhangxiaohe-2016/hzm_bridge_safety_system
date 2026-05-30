from microbit import *

display.off()
sleep(200)

buzzer = pin15

print("=== ACTIVE BUZZER TEST ===")
print("Toggling active buzzer on P15...")
print("Note: If using KittenBot IO:bit V2, check that the onboard buzzer switch is OFF if you are diagnosing P0 analog sensor. Otherwise, you can test P15 active buzzer.")

for _ in range(5):
    print("Beep!")
    buzzer.write_digital(1)
    sleep(100)
    buzzer.write_digital(0)
    sleep(400)

print("Test complete.")
