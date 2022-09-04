import falcon, json
from wsgiref.simple_server import make_server
from os import path
import os
from dotenv import load_dotenv

load_dotenv()

# load the data from the .ENV file
FILE_NAME =os.getenv('FILE_NAME')
PORT =int(os.getenv('PORT'))

# set the path to the file
file_name = path.join(path.dirname(__file__), FILE_NAME)

# create the class to handle the request
class PositionsResource(object):
    def on_get(self, req, resp):
        # check if the file exists
        if path.exists(file_name):
            with open(file_name, 'r') as json_file:
                print('fetching data from file: ' + file_name)
                trades = json.load(json_file)
        else:
            print('file not found: ' + file_name)
            trades = []
        resp.body = json.dumps(trades)

# initialize falcon
app = falcon.App()

# add routes
companies_endpoint = PositionsResource() 

# Add the route to the application
app.add_route('/positions', companies_endpoint)

#  run server
if __name__ == '__main__':
    with make_server('', PORT, app) as httpd:
        print(f'Serving on port {PORT}...')
        # Serve until process is killed
        httpd.serve_forever()