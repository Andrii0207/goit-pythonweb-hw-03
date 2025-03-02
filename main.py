from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
from pathlib import Path
import json
import datetime

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
        size = self.headers.get("Content-Length")
        body = self.rfile.read(int(size)).decode("utf-8")
        parse_body = urllib.parse.unquote_plus(body)
        r = parse_body.split("&")
        form_data = {item.split("=")[0].strip(): item.split("=")[1].strip() for item in r}
        now = datetime.datetime.now()
        str_now = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        time_form_data = {str_now: form_data}
        try:
            with open("storage/data.json", "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            loaded_data = {}
        loaded_data.update(time_form_data)

        with open(record_file_name, "w", encoding="utf-8") as file:
            json.dump(loaded_data, file, ensure_ascii=False, indent=4)

        self.send_response(302)
        self.send_header("Location", "message.html")
        self.end_headers()

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



record_file_name = "storage/data.json"


def run():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler) # noqa
    print("Starting server ... ")
    httpd.serve_forever()



if __name__=="__main__":
    run()