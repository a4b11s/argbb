from machine import Pin
import utime

import asyncio


class Button:
    def __init__(self, button: Pin):
        self.button = button
        self._pressed_times = 0
        self._is_pressed = False
        self._has_been_pressed = False
        self._pressed_at = 0
        self._pressed_time = 0
        self._last_pressed_time = 0
        self._pressed_times_threshold = 300

    def _count_presses(self):
        if self._last_pressed_time > self._pressed_times_threshold:
            self._pressed_times = 0
        else:
            self._pressed_times += 1

    @property
    def is_pressed_now(self):
        return self.button.value() == 0

    async def _loop(self):
        while True:
            self._check()
            await asyncio.sleep(0)

    def _check(self):
        if self.is_pressed_now and not self._has_been_pressed:
            self._on_press()
        elif not self.is_pressed_now and self._has_been_pressed:
            self._on_release()

    def _on_press(self):
        self._last_pressed_time = self._pressed_time
        self._count_presses()

        self._pressed_time = 0
        self._has_been_pressed = True
        self._is_pressed = True
        self._pressed_at = utime.ticks_ms()

    def _on_release(self):
        self._is_pressed = False
        self._pressed_time = utime.ticks_diff(utime.ticks_ms(), self._pressed_at)
        self._pressed_at = 0
