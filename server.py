# Python 3 server example
from dataclasses import field
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import overallOptimizer

hostName = "localhost"
serverPort = 3000

def handlePostData(data):
    print(data)

    data = json.loads(data)
    type = data['type']

    if(type == 'build'):
        input = data['data']
        message = overallOptimizer.optimizeBuild(input['weaponName'], input['weapon'], input['weaponLevel'], input['affinity'], input['isTwoHanded'], input['rollType'], input['level'], input['health'], input['endurance'], input['mind'], input['arsenalTalisman'], input['erdtreeTalisman'], input['talismans'], input['crimsonAmberMedallion'])
    else:
        message = "Hello, World! Here is a POST response"
    
    return message

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        if(self.path == '/'):
            self.path = '/index.html'

        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = post_data.decode('utf-8')

        message = handlePostData(data)

        self.send_response(200, message)
        self.send_header('Content-type','text/html')
        self.end_headers()
                
httpd = HTTPServer(('localhost',3000), Serv)
httpd.serve_forever()