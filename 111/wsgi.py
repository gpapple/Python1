from gevent.wsgi import WSGIServer
from convert.wsgi import application
import sys
HOST = '0.0.0.0'
PORT = 8000
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
WSGIServer((HOST, PORT), application).serve_forever()
