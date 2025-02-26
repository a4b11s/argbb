from utils import calc_pointer


class ModeChangeStrategy:
    def __init__(self):
        self._color_index = 0

    def change_mode(self, controller, mode_index):
        raise NotImplementedError

    def next_mode(self, controller):
        raise NotImplementedError

    def previous_mode(self, controller):
        raise NotImplementedError

    def select_mode_by_name(self, controller, mode_name):
        raise NotImplementedError

    def next_color(self, controller):
        raise NotImplementedError


class DefaultModeChangeStrategy(ModeChangeStrategy):
    def change_mode(self, controller, mode_index):
        controller.mode_index = mode_index
        controller.selected_mode = controller.modes[
            list(controller.modes.keys())[controller.mode_index]
        ]
        controller._on_mode_change()

    def next_mode(self, controller):
        mode_index = calc_pointer(controller.mode_index, 1, len(controller.modes))
        self.change_mode(controller, mode_index)

    def previous_mode(self, controller):
        mode_index = calc_pointer(controller.mode_index, -1, len(controller.modes))
        self.change_mode(controller, mode_index)

    def select_mode_by_name(self, controller, mode_name):
        if mode_name in controller.modes:
            mode_index = list(controller.modes.keys()).index(mode_name)
            self.change_mode(controller, mode_index)
        else:
            raise ValueError(f"Mode '{mode_name}' not found in available modes.")

    def next_color(self, controller):
        if controller.selected_mode.self_color_managing:
            return
        self._color_index = calc_pointer(
            self._color_index, 1, len(controller.selected_mode.color_names)
        )
        controller.selected_mode.color = controller.selected_mode.color_names[
            self._color_index
        ]
