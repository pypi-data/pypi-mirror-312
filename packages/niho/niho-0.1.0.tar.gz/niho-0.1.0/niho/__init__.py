import http.server
import socketserver

class NihoServer:
    def __init__(self):
        self.routes = {}
        self.default_status_code = 200

    def add(self, path, content):
        self.routes[path] = {"content": content, "status_code": self.default_status_code}

    def set(self, path, status_code=200, content=""):
        if path in self.routes:
            self.routes[path]["status_code"] = status_code
            self.routes[path]["content"] = content
        else:
            self.add(path, content)

    def delete(self, path):
        if path in self.routes:
            del self.routes[path]

    def run(self, ip="127.0.0.1", port=3000):
        handler = self._create_handler()
        with socketserver.TCPServer((ip, port), handler) as httpd:
            print(f"Server running at http://{ip}:{port}")
            httpd.serve_forever()

    def _create_handler(self):
        routes = self.routes

        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path in routes:
                    route = routes[self.path]
                    self.send_response(route["status_code"])
                    self.end_headers()
                    self.wfile.write(route["content"].encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")

        return CustomHandler
