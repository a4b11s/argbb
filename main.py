import neopixel
import machine
import utime
from led_effects.pulse_effect import PulseEffect
from strip import strip

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

strip.fill((0, 0, 0))
strip.write()

led_effect = PulseEffect(strip)

while True:
    led_effect.run((255, 0, 0), 10)
    print("Pulse effect done")
