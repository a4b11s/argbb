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

    async def run(self, color, sleep_ms):
        raise NotImplementedError("run() method must be implemented in subclass")

    async def _sleep(self, sleep_ms):
        await asyncio.sleep(sleep_ms / 1000)

    def _calc_brightness(self, color, brightness):
        br_percent = brightness / 100
        return tuple(int(channel * br_percent) for channel in color)
