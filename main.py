import asyncio

import machine
import neopixel
import utime

from app import App
from config import config
from modes.mode_controller import ModeController
from modes.mode_factory import ModeFactory
from wireless.wifi_manager import WiFiManager

strip_pin = int(config.get("led_pin"))  # type: ignore
strip_num_leds = int(config.get("num_leds"))  # type: ignore
name = str(config.get("name", "argbb"))

strip = neopixel.NeoPixel(machine.Pin(strip_pin), strip_num_leds)

mode_factory = ModeFactory(strip)
mode_controller = ModeController(mode_factory)
wifi_manager = WiFiManager(name, "wificred")
app = App(mode_controller, wifi_manager)


if __name__ == "__main__":
    strip.fill((255, 0, 0))
    strip.write()

    utime.sleep_ms(2000)
    app.setup()
    utime.sleep_ms(1000)
    mode_controller.select_mode_by_name("interpol")
    asyncio.run(app.run())
