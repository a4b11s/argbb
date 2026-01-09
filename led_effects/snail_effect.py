from led_effects.effect import Effect


class SnailEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")
        
        self.strip.fill(bg_color.value)  # type: ignore
        
        for i in range(tail_length.value, len(self.strip)):  # type: ignore
            # Set the head pixel (full brightness)
            self.strip[i] = color.value  # type: ignore
            
            # Clear the pixel that's now outside the tail
            clear_index = i - tail_length.value - 1  # type: ignore
            if clear_index >= 0:
                self.strip[clear_index] = bg_color.value  # type: ignore
            
            # Dim the pixel at the tail end (creates snail trail effect)
            dim_index = i - tail_length.value  # type: ignore
            if dim_index >= 0:
                self.strip[dim_index] = self._calc_brightness(color.value, 0.05)  # type: ignore

            self.strip.write()
            await self._sleep(sleep_ms.value) # type: ignore
