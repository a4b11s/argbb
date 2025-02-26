import asyncio
import socket

from wireless.body_parser import BodyParser
from utils import make_http_response, parse_http


class HTTPServer:
    def __init__(self, routes={}, body_parser: BodyParser | None = None) -> None:
        self.routes = routes
        self.body_parser = body_parser or BodyParser()

    def add_route(self, path, handler):
        self.routes[path] = handler

    async def handle_client(self, reader, writer):
        try:
            request = await reader.read(1024)
            if request:
                request = parse_http(request)
                response = self._process_request(request)
                writer.write(response if response else self.not_found())
                await writer.drain()
        except Exception as e:
            print("Error handling request:", e)
        finally:
            writer.close()
            await writer.wait_closed()

    async def host_server(self):
        await asyncio.start_server(self.handle_client, "0.0.0.0", 80)

    def _process_request(self, request):
        method, path, _, header, body = request

        if body and "Content-Type" in header:
            body = self.body_parser.parse(body, header["Content-Type"])
        else:
            body = {}

        if path in self.routes:
            return self.routes[path](method, body)
        return None

    @staticmethod
    def created(body):
        return make_http_response(status_code=201, body=body)

    @staticmethod
    def ok(body):
        return make_http_response(status_code=200, body=body)

    @staticmethod
    def not_found():
        return make_http_response(status_code=404)

    @staticmethod
    def bad_request():
        return make_http_response(status_code=400)
