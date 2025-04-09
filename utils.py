def calc_pointer(pointer: int, step: int, max_value: int) -> int:
    pointer = (pointer + step) % max_value
    if pointer < 0:
        pointer = max_value
    return pointer


def parse_http(http):
    http = http.decode("utf-8")

    parts = http.split("\r\n")
    if len(parts) < 2:
        return None, None, None, [], ""

    first_line, *headers = parts[:-1]
    body = parts[-1]
    method, path, version = first_line.split(" ")
    headers = parse_headers(headers)

    return method, path, version, headers, body


def make_http_response(status_code=200, headers=None, body=None, version="HTTP/1.1"):
    if headers is None:
        headers = []
    if body is None:
        body = b""
    if not isinstance(body, bytes):
        body = str(body).encode()
    response = b""
    response += version.encode() + b" " + str(status_code).encode() + b"\r\n"
    for header in headers:
        response += header.encode() + b"\r\n"
    response += b"\r\n"
    response += body
    return response


def parse_headers(headers):
    headers = [header for header in headers if header]
    headers = {header.split(": ")[0]: header.split(": ")[1] for header in headers}
    return headers


def noop():
    pass
