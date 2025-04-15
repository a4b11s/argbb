from led_effects.effect_factory import EffectFactory
from modes.mode import Mode
from utils import noop


class ModeFactory:
    def __init__(self, strip):
        self.strip = strip
        self.effect_factory = EffectFactory()

    def _get_mode_map(self):
        return {
            "off": lambda: Mode(self.effect_factory.create_effect("off", self.strip)),
            "interpol": lambda: Mode(
                self.effect_factory.create_effect("interpol", self.strip)
            ),
            "snail": lambda: Mode(
                self.effect_factory.create_effect("snail", self.strip)
            ),
            "pixel_madness": lambda: Mode(
                self.effect_factory.create_effect("pixel_madness", self.strip)
            ),
            "pixel_madness_bi": lambda: Mode(
                self.effect_factory.create_effect("pixel_madness_bi", self.strip)
            ),
            "snake": lambda: Mode(
                self.effect_factory.create_effect("snake", self.strip)
            ),
            "double_snake": lambda: Mode(
                self.effect_factory.create_effect("double_snake", self.strip)
            ),
            "lightningbolt": lambda: Mode(
                self.effect_factory.create_effect("lightningbolt", self.strip)
            ),
            "train": lambda: Mode(
                self.effect_factory.create_effect("train", self.strip)
            ),
            "rainbow_train": lambda: Mode(
                self.effect_factory.create_effect("rainbow_train", self.strip)
            ),
            "meteor": lambda: Mode(
                self.effect_factory.create_effect("meteor", self.strip)
            ),
            "pulse": lambda: Mode(
                self.effect_factory.create_effect("pulse", self.strip)
            ),
            "filling": lambda: Mode(
                self.effect_factory.create_effect("filling", self.strip)
            ),
            "solid": lambda: Mode(
                self.effect_factory.create_effect("solid", self.strip)
            ),
        }

    def get_available_modes(self):
        return list(self._get_mode_map().keys())

    def create_mode(self, mode_name):
        mode_map = self._get_mode_map()

        if mode_name not in mode_map:
            raise ValueError(f"Mode '{mode_name}' is not supported.")
        return mode_map.get(mode_name, noop)()
