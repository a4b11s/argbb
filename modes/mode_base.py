class ModeBase:
    def __init__(self, name, effect, speed_multiplier):
        self.name = name
        self.effect = effect
        self.speed_multiplier = speed_multiplier

    def apply(self, color, time_pointer):
        if self.effect:
            self.effect.apply(color, time_pointer)
        else:
            raise NotImplementedError("Effect not implemented")
