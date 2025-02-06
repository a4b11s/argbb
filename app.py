from machine import Pin
from led_effects.led_controller import LedController
from modes.mode_controller import ModeController
import utime
from config import DEBUG_MODE
from button import Button

class App:
    button_config = {
        "long_press": 600,
        "very_long_press": 1_000,
        "off": 20_000,
    }

    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
    }

    colors_list = list(colors.values())

    def __init__(self, controller: LedController, button_pin: Pin):
        self.controller = controller
        self.button = Button(button_pin, self.button_config)
        self.is_sleeping = False

        self.colors_pointer = 0

        self.modes = ModeController(controller)
        self.start_time = utime.ticks_ms()

    def change_speed(self):
        self.modes.change_speed()

    def change_mode(self):
        self.modes.change_mode()

    def change_color(self):
        self.colors_pointer = (self.colors_pointer + 1) % len(self.colors_list)

    def _on_short_press(self):
        self.change_speed()

    def _on_long_press(self):
        self.change_color()

    def _on_very_long_press(self):
        self.change_mode()

    def run(self):
        self.start_time = utime.ticks_ms()

        while True:
            elapsed_time = utime.ticks_diff(utime.ticks_ms(), self.start_time)
            time_pointer = elapsed_time // self.modes.get_speed()
            color = self.colors_list[self.colors_pointer]

            current_mode = self.modes.get_current_mode()
            current_mode.apply(color, time_pointer)

            self.button.button_process(
                on_short_press=self._on_short_press,
                on_long_press=self._on_long_press,
                on_very_long_press=self._on_very_long_press
            )

            if DEBUG_MODE:
                self._print_debug()
            utime.sleep_ms(10)

    def _print_debug(self):
        string = f"Speed: {self.modes.get_speed()},"
        string += f" Mode: {self.modes.get_current_mode().name},"
        string += f" Color: {self.colors_list[self.colors_pointer]},"
        string += f" Pressed: {self.button.is_pressed},"
        string += f" Pressed Time: {self.button.pressed_time}"
        string += "\r"

        print(
            string,
            end="",
        )
