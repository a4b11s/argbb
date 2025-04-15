from led_effects.effect import Effect


class FillingEffect(Effect):
    def _on_color_change(self, indx):
        self.strip.fill(self.config.get("bg_color").value)  # type: ignore
        for j in range(indx):
            self.strip[j] = self.config.get("primary_color").value  # type: ignore
        self.strip.write()
        self.color_has_changed = False

    async def _run(self):
        color = self.config.get("primary_color")
        bg_color = self.config.get("bg_color")
        sleep_ms = self.config.get("sleep_ms")

        self.strip.fill(bg_color.value)  # type: ignore
        for i in range(len(self.strip)):

            if self.color_has_changed:
                self._on_color_change(i)

            self.strip[i] = color.value  # type: ignore
            self.strip.write()
            await self._sleep(sleep_ms.value)  # type: ignore
