from machine import Pin
import utime

import asyncio


class Button:
    def __init__(self, button: Pin):
        self.button = button
        self.pressed_times = 0
        self.last_pressed_state = False
        self.pressed_times = 0

    def _check(self):
        return self.button.value()

    @property
    def is_pressed_now(self):
        return self._check() == 0

    async def _loop(self):
        while True:
            if self.is_pressed_now and not self.last_pressed_state:
                self._on_press()
            elif not self.is_pressed_now and self.last_pressed_state:
                self._on_release()
            await asyncio.sleep(0)

    def _on_press(self):
        self.pressed_times += 1
        self.last_pressed_state = True

    def _on_release(self):
        self.last_pressed_state = False
