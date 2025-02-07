import neopixel
import machine
import utime

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

strip = neopixel.NeoPixel(machine.Pin(STRIP_PIN_NUMBER), NUM_LEDS)

strip.fill((0, 0, 0))
strip.write()

while True:
    print("Blinking red")
    for i in range(NUM_LEDS):
        strip[i] = (255, 0, 0)
        strip.write()
        utime.sleep_ms(100)
    for i in range(NUM_LEDS):
        strip[i] = (0, 0, 0)
        strip.write()
        utime.sleep_ms(100)
