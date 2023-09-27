#  coding: utf-8 
import socketserver
import os
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

base_dir = './www'

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request_data = self.data.decode("utf-8").splitlines()
        method,path, _ = request_data[0].split()
        abs_path = os.path.abspath(os.path.join(base_dir,path[1:]))
        if not abs_path.startswith(os.path.abspath(base_dir)):
            body= b"404 Not Found"
            headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\n"
            response = headers.encode('utf-8') + body
            self.request.sendall(response)
        elif method != "GET":
            body = b"405 Method Not Allowed"            
            headers = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-Length: 21\r\n\r\n"
            response = headers.encode('utf-8') + body
            self.request.sendall(response)
        else:
            
            if os.path.isdir(abs_path) and not path.endswith('/'):
                location = f"http://{self.server.server_address[0]}:{self.server.server_address[1]}{path}/"
                body = b"301 Moved Permanently"
                headers = f"HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/plain\r\nContent-Length: 21\r\nLocation: {location}\r\n\r\n.encode('utf-8')"
                response = headers.encode('utf-8') + body
                self.request.sendall(response)
            elif os.path.isdir(abs_path):
                index = os.path.join(abs_path, "index.html")
                content_type, _ = mimetypes.guess_type(index)
                
                if os.path.exists(index) and os.path.isfile(index):
                    with open(index, 'rb') as file:
                        body = file.read()
                    headers = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n"
                    response = headers.encode('utf-8') + body
                    self.request.sendall(response)
                else:
                    body = b"404 Not Found"
                    headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\n"
                    response = headers.encode('utf-8') + body
                    self.request.sendall(response)
            else:
                content_type, _ = mimetypes.guess_type(abs_path)
                
                if os.path.exists(abs_path) and os.path.isfile(abs_path):
                    with open(abs_path, 'rb') as file:
                        body = file.read()
                    headers = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n"
                    response = headers.encode('utf-8') + body
                    self.request.sendall(response)
                else:
                    body = b"404 Not Found"
                    headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\n"
                    response = headers.encode('utf-8') + body
                    self.request.sendall(response)


        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
