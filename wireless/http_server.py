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

    async def _await_connection(self, server):
        while True:
            try:
                conn, addr = server.accept()
                print("Got a connection from %s" % str(addr))
                return conn, addr
            except Exception as e:
                if "EAGAIN" not in str(e):
                    raise e
                await asyncio.sleep(0.01)
                continue

    async def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        conn = None
        try:
            addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
            print("Starting server on %s" % str(addr))
            server.bind(addr)
            server.listen(5)
            while True:
                conn, request = await self._await_connection(server)
                request = conn.recv(1024)
                request = parse_http(request)
                response = self._process_request(request)
                if response:
                    conn.sendall(response)
                else:
                    conn.sendall(self.not_found())

                conn.close()

                await asyncio.sleep(0)

        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            server.close()
            if conn:
                conn.close()

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
