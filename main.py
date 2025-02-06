from app import App
from led_effects import LedController
from machine import Pin

import machine
import gc

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60


def init():
    global led_controller, button, app

    led_controller = LedController(Pin(STRIP_PIN_NUMBER), NUM_LEDS)  # type: ignore
    button = Pin(BUTTON_PIN_NUMBER, Pin.IN, Pin.PULL_UP)

    app = App(led_controller, button)


def off():
    global led_controller, app, button
    led_controller.fill((0, 0, 0))
    led_controller.pixels.write()

    del app, led_controller, button
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
    app = App(led_controller, button)
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
