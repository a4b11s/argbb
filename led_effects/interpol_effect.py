from led_effects.effect import Effect

# TODO: need to add a way to set the colors from the mode controller. Maybe different abstract class?

class InterpolEffect(Effect):
    color2 = (0, 255, 0)
    color3 = (0, 0, 255)
    steps = 80

    def _interpolate_colors(self, color1, color2, steps):

        r1, g1, b1 = color1
        r2, g2, b2 = color2

        r_diff = r2 - r1
        g_diff = g2 - g1
        b_diff = b2 - b1

        step = 1 / steps

        colors = []

        for i in range(steps + 1):
            r = int(r1 + r_diff * step * i)
            g = int(g1 + g_diff * step * i)
            b = int(b1 + b_diff * step * i)
            colors.append((r, g, b))

        return colors

    async def _run(self):
        self.strip.fill((0, 0, 0))
        colors = self._interpolate_colors(self.color, self.color2, self.steps)

        for color in colors:
            for i in range(len(self.strip)):
                self.strip[i] = color
            self.strip.write()

        
        colors = self._interpolate_colors(self.color2, self.color3, self.steps)
        for color in colors:
            for i in range(len(self.strip)):
                self.strip[i] = color
            self.strip.write()
            await self._sleep(self.sleep_ms)
            
        colors = self._interpolate_colors(self.color3, self.color, self.steps)
        for color in colors:
            for i in range(len(self.strip)):
                self.strip[i] = color
            self.strip.write()
            await self._sleep(self.sleep_ms)