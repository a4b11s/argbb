from led_effects.effect import Effect, EffectConfig


class DoubleSnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")

        # Fill background once before the loop
        self.strip.fill(bg_color.value)  # type: ignore
        
        for i in range(len(self.strip)):
            # Clear pixels that are falling off the tails
            first_tail_end = i - tail_length.value  # type: ignore
            if first_tail_end >= 0:
                self.strip[first_tail_end] = bg_color.value  # type: ignore
            
            second_tail_end = len(self.strip) - 1 - i - tail_length.value  # type: ignore
            if second_tail_end >= 0 and second_tail_end < len(self.strip):
                self.strip[second_tail_end] = bg_color.value  # type: ignore
            
            # Set the head pixels
            first_index = i
            second_index = len(self.strip) - i - 1
            
            if first_index < len(self.strip):
                self.strip[first_index] = color.value  # type: ignore
            if second_index >= 0 and second_index != first_index:
                self.strip[second_index] = color.value  # type: ignore

            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore
