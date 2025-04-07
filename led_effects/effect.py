import neopixel
import asyncio


# Need for type hinting
class IStrip(neopixel.NeoPixel):
    def __getitem__(self, key):
        return super().__getitem__(key)  # type: ignore

    def __setitem__(self, key, value):
        super().__setitem__(key, value)  # type: ignore

    def __len__(self):
        return super().__len__()  # type: ignore


class Effect:
    def __init__(self, strip):
        self.strip: IStrip = strip
        self.color = (0, 0, 0)
        self.sleep_ms = 50
        self.color_has_changed = False

    def set_color(self, color):
        self.color = color
        self.color_has_changed = True

    def set_sleep_ms(self, sleep_ms):
        self.sleep_ms = sleep_ms

    async def run(self, color, sleep_ms):
        self.set_color(color)
        self.set_sleep_ms(sleep_ms)
        await self._run()

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
