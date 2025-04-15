from .effect import Effect


class SnakeEffect(Effect):
    async def _run(self):
        color = self.config.get("primary_color")
        sleep_ms = self.config.get("sleep_ms")
        tail_length = self.config.get("tail_length")
        bg_color = self.config.get("bg_color")
        for i in range(len(self.strip)):
            self.strip.fill(bg_color.value)  # type: ignore
            for j in range(tail_length.value):  # type: ignore
                index = i + j
                if index >= len(self.strip):
                    continue
                self.strip[index] = color.value  # type: ignore
            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore
