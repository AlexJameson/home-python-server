# run 'python3 server.py'
# POST from powershell with JSON data: curl -body '{"foo": "value1", "bar": "next_value1"}' http://localhost:8000 -Method POST

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from tinydb import TinyDB, Query

DB = TinyDB('DB.json')
User = Query()
HostName = "localhost"
ServerPort = 8000
# args = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # args = {}

    # def insert_data(self, args):
        # DB.insert({'foo': 'value1', 'bar': 2}) # this is an example
		  # data = json.dumps(self.some_shit_from_self)
		  # for obj in data:
		  #     DB.insert(obj)
        # DB.insert(args)

    def delete_data(self):
        DB.purge() # remove all

    def query_all_data(self):
        print(DB.all())
        #print(len(DB)) # number of items

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes("<html><head><title>My PI server</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>GET request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<p>requestline: %s</p>" %self.requestline, "utf-8"))
        self.wfile.write(bytes("<p>command: %s</p>" %self.command, "utf-8"))
        self.wfile.write(bytes("<p>headers: %s</p>" %self.headers, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is a log for GET requests.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self._set_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
        request_data = body.decode(encoding="utf-8")
        for obj in request_data:
            DB.insert(json.loads(request_data))
    
	# for search and update see https://www.python-engineer.com/posts/tinydb/#:~:text=New%20York%27%7D)-,def%20search_user()%3A,-results%20%3D%20db

if __name__ == "__main__":        
    httpd = HTTPServer((HostName, ServerPort), SimpleHTTPRequestHandler)
    print("Server started http://%s:%s" % (HostName, ServerPort))

    try:        
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")
