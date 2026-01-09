from .effect import Effect


class SnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")
        
        # Fill background once before the loop
        self.strip.fill(bg_color.value)  # type: ignore
        
        for i in range(len(self.strip)):
            # Clear the pixel that's falling off the tail
            tail_end = i - tail_length.value  # type: ignore
            if tail_end >= 0:
                self.strip[tail_end] = bg_color.value  # type: ignore
            
            # Set the head pixel
            self.strip[i] = color.value  # type: ignore
            
            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore
