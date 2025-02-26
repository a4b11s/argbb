from utils import calc_pointer


class SpeedChangeStrategy:
    def __init__(self):
        self._speed_index = 0

    def _get_speeds(self, controller):
        return controller.selected_mode.speeds

    def change_speed(self, controller, speed_index):
        raise NotImplementedError

    def next_speed(self, controller):
        raise NotImplementedError

    def previous_speed(self, controller):
        raise NotImplementedError

    def set_own_speed(self, controller, speed):
        raise NotImplementedError


class DefaultSpeedChangeStrategy(SpeedChangeStrategy):
    def change_speed(self, controller, speed_index):
        controller.selected_mode.speed = self._get_speeds(controller)[speed_index]
        self._speed_index = speed_index

    def next_speed(self, controller):
        speed_index = calc_pointer(
            self._speed_index, 1, len(self._get_speeds(controller))
        )
        self.change_speed(controller, speed_index)

    def previous_speed(self, controller):
        speed_index = calc_pointer(
            self._speed_index, -1, len(self._get_speeds(controller))
        )
        self.change_speed(controller, speed_index)

    def set_own_speed(self, controller, speed):
        self._speed_index = 0
        controller.selected_mode.speed = speed
