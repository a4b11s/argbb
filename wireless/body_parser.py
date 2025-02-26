import json


class BodyParser:
    def parse(self, body, content_type):
        if content_type == "application/json":
            return self._parse_json(body)
        if content_type == "application/x-www-form-urlencoded":
            return self._parse_form(body)
        return body

    def _parse_json(self, body):
        return json.loads(body)

    def _parse_form(self, body):
        return {item.split("=")[0]: item.split("=")[1] for item in body.split("&")}
