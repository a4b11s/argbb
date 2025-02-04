from app import App
from led_effects import LedEffects
from machine import Pin

import machine
import gc

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60


def init():
    global led_effects, button, app

    strip_pin = Pin(STRIP_PIN_NUMBER, Pin.OUT)
    led_effects = LedEffects(strip_pin, NUM_LEDS)
    button = Pin(BUTTON_PIN_NUMBER, Pin.IN, Pin.PULL_UP)

    app = App(led_effects, button)


def off():
    global led_effects, app, button
    led_effects.fill((0, 0, 0))
    led_effects.pixels.write()

    del app, led_effects, button
    gc.collect()
    machine.Pin(BUTTON_PIN_NUMBER, machine.Pin.IN, machine.Pin.PULL_UP).irq(
        trigger=Pin.IRQ_RISING,
        handler=lambda pin: wake_up(),
    )
    machine.deepsleep()


def wake_up():
    global app, button
    init()
    button.irq(handler=None)
    app = App(led_effects, button)
    print("Woke up")
    start()


def start():
    try:
        app.run()
    except Exception as e:
        if str(e) == "OFF REQUESTED":
            off()
        else:
            raise e


if __name__ == "__main__":
    init()
    start()
