import json
from app import App
from input_controller import InputController
from led_effects import (
    pulse_effect,
    filling_effect,
    fill_effect,
    off_effect,
    meteor_effect,
    rainbow_train_effect,
    train_effect,
    lightningbolt_effect,
    snake_effect,
    double_snake_effect,
    pixel_madness_effect,
    snail_effect,
    interpol_effect,
)
from modes.mode import Mode
import asyncio
import utime
import neopixel
import machine
from config import config
from modes.mode_controller import ModeController

from wireless.wifi_manager import WiFiManager


strip_pin = int(config.get("led_pin"))  # type: ignore
strip_num_leds = int(config.get("num_leds"))  # type: ignore
name = str(config.get("name", "argbb"))

strip = neopixel.NeoPixel(machine.Pin(strip_pin), strip_num_leds)


modes = {
    "off": Mode(off_effect.OffEffect(strip)),
    "interpol": Mode(interpol_effect.InterpolEffect(strip)),
    "snail": Mode(snail_effect.SnailEffect(strip)),
    "pixel_madness": Mode(pixel_madness_effect.PixelMadnessEffect(strip)),
    "pixel_madness_bi": Mode(pixel_madness_effect.PixelMadnessBiDirectEffect(strip)),
    "snake": Mode(snake_effect.SnakeEffect(strip)),
    "double_snake": Mode(double_snake_effect.DoubleSnakeEffect(strip)),
    "lightning": Mode(lightningbolt_effect.LightningBoltEffect(strip)),
    "train": Mode(train_effect.TrainEffect(strip)),
    "rainbow_train": Mode(rainbow_train_effect.RainbowTrainEffect(strip)),
    "meteor": Mode(meteor_effect.MeteorEffect(strip)),
    "pulse": Mode(pulse_effect.PulseEffect(strip)),
    "filling": Mode(filling_effect.FillingEffect(strip)),
    "solid": Mode(fill_effect.FillEffect(strip)),
}

mode_controller = ModeController(modes)
wifi_manager = WiFiManager(name, "wificred")
app = App(mode_controller, wifi_manager)


async def setup():
    asyncio.create_task(app.setup())


async def mode_change():
    while True:
        await asyncio.sleep(20)
        app.mode_controller.next_mode()
        await asyncio.sleep(10)
        app.mode_controller.next_color()


async def main():
    asyncio.create_task(app.run())
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    strip.fill((255, 0, 0))
    strip.write()

    utime.sleep_ms(2000)
    app.synchrony_setup()
    utime.sleep_ms(1000)
    mode_controller.select_mode_by_name("interpol")
    asyncio.run(main())
