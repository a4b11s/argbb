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
    pixel_madness_effect
)
from modes.mode import Mode
import asyncio
import utime
import neopixel
import machine
from config import config
from modes.mode_controller import ModeController

from wireless.http_server import HTTPServer
from wireless.wifi_manager import WiFiManager


strip_pin = int(config.get("led_pin"))  # type: ignore
strip_num_leds = int(config.get("num_leds"))  # type: ignore
name = str(config.get("name", "argbb"))

strip = neopixel.NeoPixel(machine.Pin(strip_pin), strip_num_leds)


def update():
    from ota.ota_updater import OTAUpdater
    import gc

    try:
        import rp2

        rp2.PIO(0).remove_program()
        rp2.PIO(1).remove_program()
        print("PIO programs removed")
    except Exception as e:
        if e != "Module not found":
            print(f"Error removing PIO programs: {e}")

    gc.collect()
    print("Updating firmware...")
    otaUpdater = OTAUpdater(
        "https://github.com/a4b11s/argbb",
        main_dir="/",
        exclude_files=["wificred", "/", "config.json"],
    )

    otaUpdater.install_update_if_available()
    del otaUpdater
    machine.reset()


def set_config(data):
    if not isinstance(data, dict):
        data = json.loads(data)

    for key, value in data.items():
        config.set(key, value)

    machine.reset()


modes = {
    "off": Mode(off_effect.OffEffect(strip)),
    "pixel_madness": Mode(pixel_madness_effect.PixelMadnessEffect(strip)),
    "snake": Mode(snake_effect.SnakeEffect(strip)),
    "double_snake": Mode(double_snake_effect.DoubleSnakeEffect(strip)),
    "lightning": Mode(lightningbolt_effect.LightningBoltEffect(strip)),
    "train": Mode(train_effect.TrainEffect(strip)),
    "rainbow_train": Mode(rainbow_train_effect.RainbowTrainEffect(strip)),
    "meteor": Mode(meteor_effect.MeteorEffect(strip)),
    "pulse": Mode(pulse_effect.PulseEffect(strip)),
    "filling": Mode(filling_effect.FillingEffect(strip)),
    "fill": Mode(fill_effect.FillEffect(strip)),
}

mode_controller = ModeController(modes)
wifi_manager = WiFiManager(name, "wificred")
http_server = HTTPServer()
input_controller = InputController(
    wifi_manager,
    http_server,
    mode_controller.next_mode,
    mode_controller.previous_mode,
    mode_controller.next_speed,
    mode_controller.previous_speed,
    mode_controller.next_color,
    mode_controller.set_own_speed,
    update,
    set_config,
)

app = App(mode_controller, wifi_manager, input_controller)


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
    mode_controller.select_mode_by_name("pixel_madness")
    mode_controller.set_own_speed(50)
    asyncio.run(main())
