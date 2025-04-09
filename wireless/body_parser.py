import json


class BodyParser:
    def parse(self, body, content_type):
        if content_type == "application/json":
            return self._parse_json(body)
        if content_type == "application/x-www-form-urlencoded":
            return self._parse_form(body)
        return body  # Return as is for unsupported content types

    def _parse_json(self, body):
        try:
            return json.loads(body)
        except Exception:
            return {"error": "Invalid JSON"}

    def _parse_form(self, body):
        print(body)
        try:
            result = {}
            for item in body.split("&"):
                key_value = item.split("=")
                if len(key_value) == 2:  # Ensure both key and value exist
                    key = key_value[0]
                    value = key_value[1]
                    if key in result:
                        if isinstance(result[key], list):
                            result[key].append(value)
                        else:
                            result[key] = [result[key], value]
                    else:
                        result[key] = value
                elif (
                    len(key_value) == 1
                ):  # Handle keys without values (e.g., "key1&key2=value")
                    key = key_value[0]
                    result[key] = None
            return result
        except Exception as e:
            print(e)
            return {"error": "Invalid form data"}