import gc
from led_effects.configs import EffectConfig, InterpolEffectConfig, SnakeEffectConfig
from led_effects.effect import Effect
from led_effects.double_snake_effect import DoubleSnakeEffect
from led_effects.fill_effect import FillEffect
from led_effects.filling_effect import FillingEffect
from led_effects.interpol_effect import InterpolEffect
from led_effects.lightningbolt_effect import LightningBoltEffect
from led_effects.meteor_effect import MeteorEffect
from led_effects.off_effect import OffEffect
from led_effects.pixel_madness_effect import (
    PixelMadnessEffect,
    PixelMadnessBiDirectEffect,
)
from led_effects.pulse_effect import PulseEffect
from led_effects.rainbow_train_effect import RainbowTrainEffect
from led_effects.snail_effect import SnailEffect
from led_effects.snake_effect import SnakeEffect
from led_effects.train_effect import TrainEffect


class EffectFactory:
    def _get_effects(self):
        return {
            "double_snake": DoubleSnakeEffect,
            "fill": FillEffect,
            "filling": FillingEffect,
            "interpol": InterpolEffect,
            "lightningbolt": LightningBoltEffect,
            "meteor": MeteorEffect,
            "off": OffEffect,
            "pixel_madness": PixelMadnessEffect,
            "pixel_madness_bi": PixelMadnessBiDirectEffect,
            "pulse": PulseEffect,
            "rainbow_train": RainbowTrainEffect,
            "snail": SnailEffect,
            "snake": SnakeEffect,
            "train": TrainEffect,
        }

    def _get_configs(self):
        return {
            "double_snake": SnakeEffectConfig,
            "fill": EffectConfig,
            "filling": EffectConfig,
            "interpol": InterpolEffectConfig,
            "lightningbolt": EffectConfig,
            "meteor": EffectConfig,
            "off": EffectConfig,
            "pixel_madness": EffectConfig,
            "pixel_madness_bi": EffectConfig,
            "pulse": EffectConfig,
            "rainbow_train": EffectConfig,
            "snail": EffectConfig,
            "snake": SnakeEffectConfig,
            "train": EffectConfig,
        }

    def create_effect(self, effect_type, strip) -> Effect:
        """
        Create an effect instance with its default configuration.
        :param effect_type: The type of effect to create.
        :param strip: The LED strip instance.
        :return: An effect instance.
        """
        effects = self._get_effects()
        configs = self._get_configs()

        if effect_type not in effects:
            del effects, configs
            raise ValueError(f"{effect_type} effect not found")

        if effect_type not in configs:
            del effects, configs
            raise ValueError(f"Config for {effect_type} not found")

        effect = effects[effect_type]
        effect_config_var = configs[effect_type]

        del effects, configs
        gc.collect()

        return effect(strip, effect_config_var())
