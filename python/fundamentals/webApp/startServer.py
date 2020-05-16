import http.server
import socketserver

portInt = 8080
handlerObj = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", portInt), handlerObj) as httpd:
    print("serving at port: ", portInt)
    httpd.serve_forever()