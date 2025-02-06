import utime

class Button:
    def __init__(self, pin, config):
        self.pin = pin
        self.config = config
        self.is_pressed = False
        self.has_been_pressed = False
        self.pressed_at = 0
        self.pressed_time = 0

    def on_pressed(self):
        self.pressed_time = 0
        self.has_been_pressed = True
        self.is_pressed = True
        self.pressed_at = utime.ticks_ms()

    def on_released(self):
        self.is_pressed = False
        self.pressed_time = utime.ticks_diff(utime.ticks_ms(), self.pressed_at)
        self.pressed_at = 0

    def check_button(self):
        if self.pin.value() == 0:
            if not self.is_pressed:
                self.on_pressed()
            elif (
                utime.ticks_diff(utime.ticks_ms(), self.pressed_at)
                > self.config["off"]
            ):
                self._off()
        else:
            if self.is_pressed:
                self.on_released()

    def _off(self):
        raise Exception("OFF REQUESTED")

    def button_process(self, threshold=10, on_short_press=None, on_long_press=None, on_very_long_press=None):
        self.check_button()
        if self.pressed_time > threshold and self.has_been_pressed:
            self.has_been_pressed = False

            if self.pressed_time < self.config["long_press"]:
                if on_short_press:
                    on_short_press()
            elif self.pressed_time < self.config["very_long_press"]:
                if on_long_press:
                    on_long_press()
            else:
                if on_very_long_press:
                    on_very_long_press()
