import argparse
import io
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps

# https://dev.to/pie_tester/building-a-basic-http-server-with-python-a-guide-for-automation-and-prototyping-4967


class Server(HTTPServer):
    def __init__(self, address, request_handler):
        super().__init__(address, request_handler)


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server_class):
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            count = get_hit_count()
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        response = {"message": "Hello world"}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(dumps(response))))
        self.end_headers()
        self.wfile.write(str(response).encode('utf8'))

    def response_body(encoding=None):
        encoding = io.text_encoding(encoding)
        with open("/home/max/Development/demopythonwebserver/index.html", encoding) as f:
            return f.read()


def start_server(addr, port, server_class=Server, handler_class=RequestHandler):
    server_settings = (addr, port)
    http_server = server_class(server_settings, handler_class)
    print(f"Starting server on {addr}:{port}")
    http_server.serve_forever()


def get_hit_count():
    retries = 5
    cache = redis.Redis(host='redis', port=6379)
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Run a simple HTTP server.")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",
        help="Specify the IP address which server should listen",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=80,
        help="Specify the port which server should listen",
    )
    args = parser.parse_args()
    start_server(addr=args.listen, port=args.port)


if __name__ == "__main__":
    main()
