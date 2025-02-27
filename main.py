from app import App
from input_controller import InputController
from led_effects import pulse_effect, filling_effect, fill_effect, off_effect, meteor_effect
from modes.mode import Mode
from strip import strip
import asyncio
import utime
from modes.mode_controller import ModeController

from wireless.http_server import HTTPServer
from wireless.wifi_manager import WiFiManager

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

modes = {
    "off": Mode(off_effect.OffEffect(strip)),
    "meteor": Mode(meteor_effect.MeteorEffect(strip)),
    "pulse": Mode(pulse_effect.PulseEffect(strip)),
    "filling": Mode(filling_effect.FillingEffect(strip)),
    "fill": Mode(fill_effect.FillEffect(strip)),
}

mode_controller = ModeController(modes)
wifi_manager = WiFiManager("argbb", "wificred", "argbb")
http_server = HTTPServer()
input_controller = InputController(
    wifi_manager,
    http_server,
    mode_controller.next_mode,
    mode_controller.previous_mode,
    mode_controller.next_speed,
    mode_controller.previous_speed,
    mode_controller.next_color,
)

app = App(mode_controller, wifi_manager, input_controller)
mode_controller.select_mode_by_name("meteor")
mode_controller.set_own_speed(10)

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
    strip.fill((0, 0, 0))
    strip.write()

    utime.sleep_ms(1000)
    app.synchrony_setup()
    asyncio.run(main())
