import SocketServer

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

if __name__ == "__main__":
    HOST, PORT = 'localhost', 8000

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    server.serve_forever()
