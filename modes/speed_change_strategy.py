from utils import calc_pointer


class SpeedChangeStrategy:
    def __init__(self, controller):
        self.controller = controller
        self._speed_index = 0

    def _get_speeds(self):
        return self.controller.selected_mode.speeds

    def change_speed(self, speed_index):
        raise NotImplementedError

    def next_speed(self):
        raise NotImplementedError

    def previous_speed(self):
        raise NotImplementedError

    def set_own_speed(self, speed):
        raise NotImplementedError


class DefaultSpeedChangeStrategy(SpeedChangeStrategy):
    def change_speed(self, speed_index):
        self.controller.selected_mode.speed = self._get_speeds()[speed_index]
        self._speed_index = speed_index

    def next_speed(self):
        speed_index = calc_pointer(
            self._speed_index, 1, len(self._get_speeds())
        )
        self.change_speed(speed_index)

    def previous_speed(self):
        speed_index = calc_pointer(
            self._speed_index, -1, len(self._get_speeds())
        )
        self.change_speed(speed_index)

    def set_own_speed(self, speed):
        self._speed_index = 0
        self.controller.selected_mode.speed = speed
