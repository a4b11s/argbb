from led_effects.base_effect import BaseEffect


class FillEffect(BaseEffect):
    def apply(self, color, *args, **kwargs):
        self.controller.fill(color)
