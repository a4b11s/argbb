from .effect import Effect


class SnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = int(self.config.get("sleep_ms"))
        tail_length = int(self.config.get("tail_length"))
        bg_color = self.config.get("bg_color")
        for i in range(len(self.strip)):
            self.strip.fill(bg_color)
            for j in range(tail_length):
                index = i + j
                if index >= len(self.strip):
                    continue
                self.strip[index] = color
            self.strip.write()
            await self._sleep(sleep_ms)
