# Usage: python3 serve.py

import http.server

file_map = {
    '/revshell': './uploads/reverse-shell.php',
    '/linpeas': './uploads/linpeas.sh',
    '/pspy': './uploads/pspy64'
}

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in file_map.keys():
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            with open(file_map[self.path], 'rb') as f:
                self.wfile.write(f.read())
        else:
            print('nope')

httpd = http.server.HTTPServer(('10.10.14.172', 8000), RequestHandler)

httpd.serve_forever()