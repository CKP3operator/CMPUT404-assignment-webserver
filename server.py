#  coding: utf-8 
import socketserver
import os
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

folderServe = os.path.join(os.path.dirname(__file__), 'www')

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        request_lines = self.data.decode().split('\r\n')
        method,path,protocol = request_lines[0].split()
        if method != 'GET':
            response = f"HTTP/1.1 405 Method Not Allowed\r\n\r\n<h1>405 Method Not Allowed</h1>"
            self.request.sendall(response.encode())
        elif method == 'GET' and path != '/' and os.path.isdir(os.path.join(folderServe, path.lstrip('/'))) and not path.endswith('/'):
            new_location = path + '/'
            response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {new_location}\r\n\r\n"
            self.request.sendall(response.encode())
        else:
            if path == '/':
                request_path = os.path.join(folderServe, 'index.html')
                if os.path.exists(request_path) and os.path.isfile(request_path):
                    with open(request_path, 'rb') as file:
                        response_data = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_data)}\r\n\r\n"
                    self.request.sendall(response.encode() + response_data)
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                    self.request.sendall(response.encode())
            
            else:
                request_path = os.path.join(folderServe, path.lstrip('/'))
                if os.path.exists(request_path) and os.path.isfile(request_path) and request_path.startswith(folderServe):
                    with open(request_path, 'rb') as file:
                        response_data = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_data)}\r\n\r\n"
                    self.request.sendall(response.encode() + response_data)
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
                    self.request.sendall(response.encode())
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
