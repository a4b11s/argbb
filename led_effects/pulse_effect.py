from led_effects.led_effect import LedEffect
import utime


class PulseEffect(LedEffect):
    def __init__(self, strip):
        super().__init__(strip)
        self._brightness_steps = 100

    @property
    def brightness_steps(self):
        return self._brightness_steps

    @brightness_steps.setter
    def brightness_steps(self, value):
        self._brightness_steps = value

    def run(self, color, sleep_ms):
        for i in range(1, self._brightness_steps):
            self._step(color, i, sleep_ms)
        for i in range(self._brightness_steps, 0, -1):
            self._step(color, i, sleep_ms)

    def _calculate_brightness(self, color, brightness):
        br_percent = brightness / self._brightness_steps
        return tuple(int(channel * br_percent) for channel in color)

    def _step(self, color, step, sleep_ms):
        br_color = self._calculate_brightness(color, step)
        self.strip.fill(br_color)
        self.strip.write()
        utime.sleep_ms(sleep_ms)
