import SimpleHTTPServer
import SocketServer
import cgi
import urlparse

PORT = 8000

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	
	def do_POST(s):
			"""Respond to a POST request."""

			# Extract and print the contents of the POST
			length = int(s.headers['Content-Length'])
			post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
			for key, value in post_data.iteritems():
				print "%s=%s" % (key, value)

			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()
			s.wfile.write('[{ready: "new", location: "lab"}]')
			
Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()