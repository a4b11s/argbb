import socket

from utils import make_http_response, parse_http


class HTTPServer:
    def __init__(self, routes={}) -> None:
        self.routes = routes

    def add_route(self, path, handler):
        self.routes[path] = handler

    def _await_connection(self, server):
        conn, addr = server.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        request = parse_http(request)
        return conn, request

    def host_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = None
        try:
            addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
            server.bind(addr)
            server.listen(5)
            while True:
                conn, request = self._await_connection(server)
                response = self._proccess_request(request)

                if response:
                    conn.sendall(response)
                else:
                    conn.sendall(make_http_response(status_code=404))

                conn.close()

        except KeyboardInterrupt:
            print("Server stopped")
        finally:
            server.close()
            if conn:
                conn.close()

    def _proccess_request(self, request):
        method, path, _, _, body = request
        if path in self.routes:
            return self.routes[path](method, body)
        return None
