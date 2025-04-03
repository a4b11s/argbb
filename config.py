import json


class Config:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

        if self.config is None:
            self.create_default_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    def get(self, key, default=None) -> str | int | None:
        return self.config.get(key, default)  # type: ignore

    def set(self, key, value):
        self.config[key] = value  # type: ignore
        self.save_config()

    def save_config(self):
        try:
            with open(self.config_path, "w") as file:
                json.dump(self.config, file)
        except Exception as e:
            print(f"Error saving config: {e}")

    def create_default_config(self):
        default_config = {
            "led_pin": 15,
            "num_leds": 60,
            "name": "argbb",
        }

        self.config = default_config
        self.save_config()


config = Config()
