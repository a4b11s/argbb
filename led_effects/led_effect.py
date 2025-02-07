import neopixel


# Need for type hinting
class IStrip(neopixel.NeoPixel):
    def __getitem__(self, key):
        return super().__getitem__(key)  # type: ignore

    def __setitem__(self, key, value):
        super().__setitem__(key, value)  # type: ignore


class LedEffect:
    def __init__(self, strip):
        self.strip: IStrip = strip

    def run(self):
        raise NotImplementedError("run() method must be implemented in subclass")
