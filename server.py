#Garrett Webb
#gswebb
#CSE138 Kuper Spring 2021

#acknowledgements
#https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#https://docs.python.org/3/library/http.server.html
#https://stackoverflow.com/questions/31371166/reading-json-from-simplehttpserver-post-data


import sys
import http.server
import socketserver
import json
from sys import argv
kvstore = {}

class requestHandler(http.server.BaseHTTPRequestHandler):
    kvstore = {}
    def _set_headers(self, response_code):
        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        print("GET: unimplelmented")
        self._set_headers(response_code=500)
        return
    
    # this is here as legacy in case we need to reuse any of the code
    # just collapse the function in VScode
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

    def do_PUT(self):
        if str(self.path).startswith("/key-value-store/"):
            #get the substring after the /ping/
            response_str = str(self.path).split("/key-value-store/",1)[1]
            if(len(response_str) > 0 and len(response_str) < 50):
                self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = json.loads(self.data_string)
                if "value" not in data:
                    self._set_headers(response_code=400)
                    response = bytes(json.dumps({'error' : "Value is missing", 'message' : "Error in PUT"}), 'utf-8')
                elif response_str in kvstore:
                    kvstore[response_str] = data["value"]
                    self._set_headers(response_code=200)
                    response = bytes(json.dumps({'message' : "Updated successfully", 'replaced' :True}), 'utf-8')
                else:
                    kvstore[response_str] = data["value"]
                    self._set_headers(response_code=201)
                    response = bytes(json.dumps({'message' : "Added successfully", 'replaced' :False}), 'utf-8')
            elif (len(response_str) > 50):
                self._set_headers(response_code=400)
                response = bytes(json.dumps({'error' : "Key is too long", 'message' : "Error in PUT"}), 'utf-8')
            
            self.wfile.write(response)
        
        else:
            #default 500 code to clean up loose ends
            self._set_headers(response_code=500)

        return
    
    def do_DELETE(self):
        print("DELETE: unimplelmented")
        self._set_headers(response_code=500)
        return

def run(server_class=http.server.HTTPServer, handler_class=requestHandler, addr='', port=8085):
    # this function initializes and runs the server on the class defined above
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    kvstore = {}
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