import gc
import asyncio

from led_effects.configs import EffectConfig
import neopixel


# Need for type hinting
class IStrip(neopixel.NeoPixel):
    def __getitem__(self, key):
        return super().__getitem__(key)  # type: ignore

    def __setitem__(self, key, value):
        super().__setitem__(key, value)  # type: ignore

    def __len__(self):
        return super().__len__()  # type: ignore


class Effect:
    def __init__(self, strip, config: EffectConfig):
        self.strip: IStrip = strip
        self.config = config
        self.color_has_changed = False

    def set_config(self, config: EffectConfig):
        self.config = config
        self.color_has_changed = True

    async def run(self):
        await self._run()
        gc.collect()

    async def _run(self):
        raise NotImplementedError("run() method must be implemented in subclass")

    async def _sleep(self, sleep_ms):
        await asyncio.sleep(sleep_ms / 1000)

    def _calc_brightness(self, color, brightness):
        """
        Calculate the brightness of a color.
        :param color: The RGB color tuple.
        :param brightness: The brightness percentage (0-1).
        :return: The adjusted RGB color tuple.
        """
        return tuple(int(channel * brightness) for channel in color)
