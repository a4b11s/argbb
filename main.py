from app import App
from led_effects import pulse_effect, filling_effect, fill_effect
from modes.mode import Mode
from strip import strip
import asyncio
import utime
from mode_controller import ModeController

BUTTON_PIN_NUMBER = 16
STRIP_PIN_NUMBER = 15
NUM_LEDS = 60

modes = {
    "pulse": Mode(pulse_effect.PulseEffect(strip)),
    "filling": Mode(filling_effect.FillingEffect(strip)),
    "fill": Mode(fill_effect.FillEffect(strip)),
}

mode_controller = ModeController(modes)

app = App(mode_controller)


if __name__ == "__main__":
    strip.fill((0, 0, 0))
    strip.write()

    utime.sleep_ms(1000)
    asyncio.run(app.run())
