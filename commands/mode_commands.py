from commands.command import Command


class NextModeCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.next_mode()


class PreviousModeCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.previous_mode()


class NextSpeedCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.next_speed()


class PreviousSpeedCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.previous_speed()


class NextColorCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.next_color()


class PreviousColorCommand(Command):
    def __init__(self, mode_controller):
        self.mode_controller = mode_controller

    def execute(self):
        self.mode_controller.previous_color()


class SetSpeedCommand(Command):
    def __init__(self, mode_controller, speed):
        self.mode_controller = mode_controller
        self.speed = speed

    def execute(self):
        self.mode_controller.set_own_speed(self.speed)


class SetModeCommand(Command):
    def __init__(self, mode_controller, mode_name):
        self.mode_controller = mode_controller
        self.mode_name = mode_name

    def execute(self):
        self.mode_controller.select_mode_by_name(self.mode_name)


class UpdateConfigCommand(Command):
    def __init__(self, mode_controller, data):
        self.mode_controller = mode_controller
        self.data = data
    def execute(self):
        self.mode_controller.update_mode_config(self.data)