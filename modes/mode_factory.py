from led_effects import (
    double_snake_effect,
    fill_effect,
    filling_effect,
    interpol_effect,
    lightningbolt_effect,
    meteor_effect,
    off_effect,
    pixel_madness_effect,
    pulse_effect,
    rainbow_train_effect,
    snail_effect,
    snake_effect,
    train_effect,
)
from modes.mode import Mode
from utils import noop


class ModeFactory:
    def __init__(self, strip):
        self.strip = strip

    def _get_mode_map(self):
        return {
            "off": lambda: Mode(off_effect.OffEffect(self.strip)),
            "interpol": lambda: Mode(interpol_effect.InterpolEffect(self.strip)),
            "snail": lambda: Mode(snail_effect.SnailEffect(self.strip)),
            "pixel_madness": lambda: Mode(
                pixel_madness_effect.PixelMadnessEffect(self.strip)
            ),
            "pixel_madness_bi": lambda: Mode(
                pixel_madness_effect.PixelMadnessBiDirectEffect(self.strip)
            ),
            "snake": lambda: Mode(snake_effect.SnakeEffect(self.strip)),
            "double_snake": lambda: Mode(
                double_snake_effect.DoubleSnakeEffect(self.strip)
            ),
            "lightning": lambda: Mode(
                lightningbolt_effect.LightningBoltEffect(self.strip)
            ),
            "train": lambda: Mode(train_effect.TrainEffect(self.strip)),
            "rainbow_train": lambda: Mode(
                rainbow_train_effect.RainbowTrainEffect(self.strip)
            ),
            "meteor": lambda: Mode(meteor_effect.MeteorEffect(self.strip)),
            "pulse": lambda: Mode(pulse_effect.PulseEffect(self.strip)),
            "filling": lambda: Mode(filling_effect.FillingEffect(self.strip)),
            "solid": lambda: Mode(fill_effect.FillEffect(self.strip)),
        }

    def get_available_modes(self):
        return list(self._get_mode_map().keys())

    def create_mode(self, mode_name):
        mode_map = self._get_mode_map()

        if mode_name not in mode_map:
            raise ValueError(f"Mode '{mode_name}' is not supported.")
        return mode_map.get(mode_name, noop)()
