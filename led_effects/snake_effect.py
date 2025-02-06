from base_effect import BaseEffect

class SnakeEffect(BaseEffect):
    def apply(self, color, length=5, step=0, *args, **kwargs):
        step, backward = self._calculate_step(step, length)
        self.controller.clear()
        self._draw_snake(color, length, step, backward)
        self.controller.write()

    def _calculate_step(self, step, length):
        step = step % (self.controller.num_leds + length)
        backward = step >= self.controller.num_leds
        step = step % self.controller.num_leds
        return step, backward

    def _draw_snake(self, color, length, step, backward):
        for j in range(length):
            index = step - j if not backward else step + j
            if 0 <= index < self.controller.num_leds:
                self.controller[index] = color  # type: ignore
