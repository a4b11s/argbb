from led_effects.led_controller import LedControllerInterface

class BaseEffect:
    def __init__(self, controller: LedControllerInterface):
        self.controller = controller

    def apply(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")
