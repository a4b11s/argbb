class Field:
    """
    Represents a configurable field with metadata for UI representation.
    """

    def __init__(
        self, value, val_type: "int" | "string" | "color" | "array" | "float", name, description  # type: ignore
    ):
        self._value = value  # The actual value of the field
        self.name = name  # The display name of the field
        self.description = description  # A description of the field for UI
        self.val_type = val_type

    def _cast_type(self, value, val_type):
        """
        Cast the given value to the specified type.
        """
        if val_type == "int":
            return int(value)
        elif val_type == "float":
            return float(value)
        elif val_type == "string":
            return str(value)
        elif val_type == "color":
            if (
                isinstance(value, tuple)
                and len(value) == 3
                or isinstance(value, list)
                and len(value) == 3
            ):
                print(value)
                return tuple(map(int, value))
            else:
                raise ValueError(
                    "Invalid color format. Expected a tuple of 3 integers."
                )
        elif val_type == "array":
            if isinstance(value, list):
                return list(value)
            else:
                raise ValueError("Invalid array format. Expected a list.")
        else:
            raise TypeError(f"Unsupported type: {val_type}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = self._cast_type(val, self.val_type)


class EffectConfig:
    """
    Base configuration class for effects.
    """

    def __init__(self, color=(255, 0, 0), bg_color=(0, 0, 0), sleep_ms=50):
        self.fields: dict[str, Field] = {
            "primary_color": Field(
                color, "color", "Primary color", "The RGB primary color of the effect"
            ),
            "sleep_ms": Field(
                sleep_ms,
                "int",
                "Sleep Time (ms)",
                "The delay between updates in milliseconds",
            ),
            "bg_color": Field(
                bg_color,
                "color",
                "Background color",
                "The RGB background color of the effect",
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
        return self.fields.get(key)  # type: ignore

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
                    "int",
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
                    "array",
                    "colors_array",
                    "The RGB color array for interpolate between them",
                ),
                "interpolate_steps": Field(
                    interpolate_steps,
                    "int",
                    "interpolate_steps",
                    "The number of steps to interpolate between colors in the color array",
                ),
            }
        )


class LightningBoltEffectConfig(EffectConfig):
    def __init__(
        self,
        color=(255, 0, 0),
        bg_color=(0, 0, 0),
        sleep_ms=50,
        min_brightness=1,
        max_brightness=100,
        min_await_between_bolts=100,
        max_await_between_bolts=1000,
        min_await_between_flashes=10,
        max_await_between_flashes=50,
        min_flashes=1,
        max_flashes=5,
        min_flashes_time=1,
        max_flashes_time=200,
    ):
        super().__init__(color, bg_color, sleep_ms)
        self.fields.update(
            {
                "min_brightness": Field(
                    min_brightness,
                    "int",
                    "min_brightness",
                    "The minimum brightness of the lightning bolt effect",
                ),
                "max_brightness": Field(
                    max_brightness,
                    "int",
                    "max_brightness",
                    "The maximum brightness of the lightning bolt effect",
                ),
                "min_await_between_bolts": Field(
                    min_await_between_bolts,
                    "int",
                    "min_await_between_bolts",
                    "The minimum time to wait between lightning bolts (ms)",
                ),
                "max_await_between_bolts": Field(
                    max_await_between_bolts,
                    "int",
                    "max_await_between_bolts",
                    "The maximum time to wait between lightning bolts (ms)",
                ),
                "min_await_between_flashes": Field(
                    min_await_between_flashes,
                    "int",
                    "min_await_between_flashes",
                    "The minimum time to wait between flashes in a bolt (ms)",
                ),
                "max_await_between_flashes": Field(
                    max_await_between_flashes,
                    "int",
                    "max_await_between_flashes",
                    "The maximum time to wait between flashes in a bolt (ms)",
                ),
                "min_flashes": Field(
                    min_flashes,
                    "int",
                    "min_flashes",
                    "The minimum number of flashes in a lightning bolt",
                ),
                "max_flashes": Field(
                    max_flashes,
                    "int",
                    "max_flashes",
                    "The maximum number of flashes in a lightning bolt",
                ),
                "min_flashes_time": Field(
                    min_flashes_time,
                    "int",
                    "min_flashes_time",
                    "The minimum duration of a flash (ms)",
                ),
                "max_flashes_time": Field(
                    max_flashes_time,
                    "int",
                    "max_flashes_time",
                    "The maximum duration of a flash (ms)",
                ),
            }
        )


class MeteorEffectConfig(EffectConfig):
    def __init__(
        self,
        color=(255, 0, 0),
        bg_color=(0, 0, 0),
        sleep_ms=50,
        tail_length=50,
        fade_factor=[0.7, 0.9],
        spark_probability=0.1,
    ):
        super().__init__(color, bg_color, sleep_ms)
        self.fields.update(
            {
                "tail_length": Field(
                    tail_length,
                    "int",
                    "tail_length",
                    "The length of the snake tail effect in the LED animation",
                ),
                "fade_factor": Field(
                    fade_factor,
                    "array",
                    "fade_factor",
                    "The range of fade factors for the meteor effect",
                ),
                "spark_probability": Field(
                    spark_probability,
                    "float",
                    "spark_probability",
                    "The probability of a spark appearing in the meteor effect",
                ),
            }
        )


class TrainEffectConfig(EffectConfig):
    def __init__(
        self, color=(255, 0, 0), bg_color=(0, 0, 0), sleep_ms=50, car_size=4, gap=1
    ):
        super().__init__(color, bg_color, sleep_ms)
        self.fields.update(
            {
                "car_size": Field(
                    car_size,
                    "int",
                    "car_size",
                    "The size of each car in the train effect",
                ),
                "gap": Field(
                    gap,
                    "int",
                    "gap",
                    "The gap between cars in the train effect",
                ),
            }
        )
