'''
Author: Rudy DeSanti
Last Modified: September 29, 2022
Description: Webserver using Flask. Serves HTML file built using React found at path 'react/build-optimizer-react/build'. Supports GET and POST requests. Runs on port 5000.
'''
import os
from flask import Flask, send_from_directory, request
import serverMethods as server

app = Flask(__name__, static_folder='react/build-optimizer-react/build')

# Serve React App
@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        """return the information for <user_id>"""
        data = request.get_json(force=True)
        print(data['type'])
        return server.handleType(data)

    elif request.method == 'GET':
        return send_from_directory(app.static_folder, 'index.html')
    else:
        # POST Error 405 Method Not Allowed
        print("Error 405")
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
