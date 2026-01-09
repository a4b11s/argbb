from led_effects.effect import Effect


class InterpolEffect(Effect):
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
        colors_array = self.config.get("colors_array").value.copy()  # type: ignore
        colors_array.append(colors_array[0])

        sleep_ms = self.config.get("sleep_ms")
        interpolate_steps = self.config.get("interpolate_steps")
        colors_array_length = len(colors_array)
        strip_len = len(self.strip)
        
        for i in range(colors_array_length - 1):
            colors = self._interpolate_colors(
                colors_array[i], colors_array[i + 1], interpolate_steps.value  # type: ignore
            )

            for color in colors:
                # Fill the entire strip at once instead of pixel by pixel
                self.strip.fill(color)
                self.strip.write()
                await self._sleep(sleep_ms.value)  # type: ignore

        del colors_array
