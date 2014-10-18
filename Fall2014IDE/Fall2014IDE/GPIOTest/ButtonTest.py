import RPi.GPIO as GPIO
import time
import uinput

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

device = uinput.Device([uinput.KEY_A])

isPussy = True

def buttonCallback(channel):
    print(channel)
    device.emit_click(uinput.KEY_A)
    print("\n")
    print("Weed")

GPIO.add_event_detect(40, GPIO.BOTH, callback=buttonCallback, bouncetime=300)

while True:
    if isPussy:
        print("Pussy")

    else:
        print("Money")

    isPussy = not isPussy
    time.sleep(0.3)