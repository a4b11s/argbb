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
