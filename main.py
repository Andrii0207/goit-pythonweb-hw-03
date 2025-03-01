from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from mimetypes import guess_type
from pathlib import Path
import mimetypes

BASE_DIR = Path(__file__).parent

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self): # noqa
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case "/":
                self.send_html("index.html")
            case "/message.html":
                self.send_html("message.html")
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html", 404)

    def do_POST(self):  # noqa
        pass

    def send_html(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status=200):
        self.send_response(status)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-type', mime_type)
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())




def run():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler) # noqa
    print("Starting server ... ")
    httpd.serve_forever()



if __name__=="__main__":
    run()