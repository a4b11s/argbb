class Field:
    """
    Represents a configurable field with metadata for UI representation.
    """

    def __init__(self, value, name, description):
        self.value = value  # The actual value of the field
        self.name = name  # The display name of the field
        self.description = description  # A description of the field for UI


class EffectConfig:
    """
    Base configuration class for effects.
    """

    def __init__(self, color=(255, 0, 0), bg_color=(0, 0, 0), sleep_ms=50):
        self.fields = {
            "primary_color": Field(
                color, "Primary color", "The RGB primary color of the effect"
            ),
            "sleep_ms": Field(
                sleep_ms, "Sleep Time (ms)", "The delay between updates in milliseconds"
            ),
            "bg_color": Field(
                bg_color, "Background color", "The RGB background color of the effect"
            ),
        }

    def update_fields(self, updates: dict):
        """
        Dynamically update the fields of the configuration.
        :param updates: A dictionary where keys are field names and values are the new values.
        """
        for field_name, new_value in updates.items():
            if field_name in self.get_fields():
                field = self.fields[field_name]
                field.value = new_value
            else:
                raise AttributeError(
                    f"{field_name} does not exist in the configuration"
                )

    def get(self, key):
        return self.fields.get(key).value  # type: ignore

    def get_fields(self):
        """
        Retrieve the list of field names.

        Returns:
            list: A list containing the keys of the `fields` dictionary.
        """
        return list(self.fields.keys())


class SnakeEffectConfig(EffectConfig):
    def __init__(
        self,
        color=(255, 0, 0),
        bg_color=(0, 0, 0),
        sleep_ms=50,
        tail_length=5,
    ):
        super().__init__(color, bg_color, sleep_ms)
        self.fields.update(
            {
                "tail_length": Field(
                    tail_length,
                    "tail_length",
                    "The length of the snake tail effect in the LED animation",
                )
            }
        )


class InterpolEffectConfig(EffectConfig):
    def __init__(
        self,
        color=(255, 0, 0),
        bg_color=(0, 0, 0),
        sleep_ms=50,
        colors_array=None,
        interpolate_steps=80,
    ):
        super().__init__(color, bg_color, sleep_ms)
        if colors_array is None:
            colors_array = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        self.fields.update(
            {
                "colors_array": Field(
                    colors_array,
                    "colors_array",
                    "The RGB color array for interpolate between them",
                ),
                "interpolate_steps": Field(
                    interpolate_steps,
                    "interpolate_steps",
                    "The number of steps to interpolate between colors in the color array",
                ),
            }
        )
