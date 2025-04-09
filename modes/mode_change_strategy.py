from utils import calc_pointer


class ModeChangeStrategy:
    def __init__(self, controller):
        self.controller = controller
        self._color_index = 0

    def change_mode(self, mode_index):
        raise NotImplementedError

    def next_mode(self):
        raise NotImplementedError

    def previous_mode(self):
        raise NotImplementedError

    def select_mode_by_name(self, mode_name):
        raise NotImplementedError

    def next_color(self):
        raise NotImplementedError

    def previous_color(self):
        raise NotImplementedError


class DefaultModeChangeStrategy(ModeChangeStrategy):
    def __init__(self, controller):
        super().__init__(controller)

        self.modes = self.controller.get_available_modes()

    def change_mode(self, mode_index):
        self.controller.mode_index = mode_index
        self.controller.selected_mode = self.controller.mode_factory.create_mode(
            self.controller.get_available_modes()[self.controller.mode_index]
        )
        self.controller._on_mode_change()

    def next_mode(self):
        mode_index = calc_pointer(
            self.controller.mode_index, 1, len(self.modes)
        )
        self.change_mode(mode_index)

    def previous_mode(self):
        mode_index = calc_pointer(
            self.controller.mode_index, -1, len(self.modes)
        )
        self.change_mode(mode_index)

    def select_mode_by_name(self, mode_name):
        if mode_name in self.modes:
            mode_index = self.modes.index(mode_name)
            self.change_mode(mode_index)
        else:
            raise ValueError(f"Mode '{mode_name}' not found in available modes.")

    def next_color(self):
        if self.controller.selected_mode.self_color_managing:
            return
        self._color_index = calc_pointer(
            self._color_index, 1, len(self.controller.selected_mode.color_names)
        )
        self.controller.selected_mode.color = self.controller.selected_mode.color_names[
            self._color_index
        ]

    def previous_color(self):
        if self.controller.selected_mode.self_color_managing:
            return
        self._color_index = calc_pointer(
            self._color_index, -1, len(self.controller.selected_mode.color_names)
        )
        self.controller.selected_mode.color = self.controller.selected_mode.color_names[
            self._color_index
        ]
