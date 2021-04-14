#Garrett Webb
#gswebb
#CSE138 Kuper Spring 2021

#acknowledgements
#https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#https://docs.python.org/3/library/http.server.html

import sys
import http.server
import socketserver
import json
from sys import argv

class requestHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self, response_code):
        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if str(self.path) == '/ping': 
            #if there is something after the ping, this will not trigger

            #send the 200 code
            self._set_headers(response_code=200)

            #send the json thing
            response = bytes(json.dumps({'message' : "I'm alive!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            #if the string is not exactly /ping but starts with it, not allowed
            self._set_headers(response_code=405)
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)

        elif str(self.path) == '/echo':
            #not a ping, but an echo
            self._set_headers(response_code=200)
            response = bytes(json.dumps({'message' : "Get Message Received"}), 'utf-8')
            self.wfile.write(response)

        else:
            #default 500, just for cleaning up loose ends
            self._set_headers(response_code=500)

        return
    
    def do_POST(self):
        if str(self.path) == '/ping':
            #if there is something after the ping, this will not trigger
            self._set_headers(response_code=405)
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            #if starts with ping, but has something after, send 200
            self._set_headers(response_code=200)
            #get the substring after the /ping/
            response_str = str(self.path).split("/ping/",1)[1]
            response = bytes(json.dumps({'message' : "I'm alive, " + response_str + "!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path) == '/echo':
            # not a ping, but an echo
            self._set_headers(response_code=400)
            response = bytes("Bad Request", 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/echo?"):
            # echo with a message
            self._set_headers(response_code=200)
            #get the message from the echo
            response_str = str(self.path).split("/echo?msg=",1)[1]
            response = bytes(json.dumps({'message' : response_str}), 'utf-8')
            self.wfile.write(response)

        else:
            #default 500 code to clean up loose ends
            self._set_headers(response_code=500)

        return

def run(server_class=http.server.HTTPServer, handler_class=requestHandler, addr='', port=8085):
    # this function initializes and runs the server on the class defined above
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    
    try:
        print(f"Starting HTTP server on {addr}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':

    if len(argv) == 2:
        #call the run function with custom port
        run(port=int(argv[1]))
    else:
        #call the run function with default port 8085
        run()