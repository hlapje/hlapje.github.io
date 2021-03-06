import os
import sys
import SimpleHTTPServer
import BaseHTTPServer
import SocketServer

class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.redirect():
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        if not self.redirect():
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_HEAD(self)

    def redirect(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for base in "index", "default":
                for ext in ".html", ".htm", ".txt":
                    index = base+ext
                    index_path = os.path.join(path, index)
                    if os.path.exists(index_path):
                        new_path = self.path
                        if not new_path.endswith('/'):
                            new_path += '/'
                        new_path += index

                        self.send_response(302)
                        self.send_header("Location", new_path)
                        self.end_headers()
                        return True
        return False

PORT = 80
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    pass
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
