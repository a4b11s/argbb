from config import LED_PIN, NUM_LEDS
import neopixel
import machine

strip = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)
