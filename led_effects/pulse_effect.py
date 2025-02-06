from base_effect import BaseEffect

class PulseEffect(BaseEffect):
    def apply(self, color, step=0):
        step = self._normalize_step(step)
        color = self._scale_color(color, step)
        self.controller.fill(color)

    def _normalize_step(self, step):
        return step % 512

    def _scale_color(self, color, step):
        step = step if step < 256 else 511 - step
        return tuple(int(c * step / 255) for c in color)
