import subprocess
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    _host = None

    def _get_host(self):
        if self._host:
            return self._host
        with open("/config/config.yaml", 'r') as stream:
            try:
                self._host = yaml.load(stream)['host']
                return self._host
            except (yaml.YAMLError, OSError):
                return None

    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        try:
            host = self._get_host()

            if host:
                result = subprocess.run(['ink', '-b',
                                         'bjnp://{0}'.format(host)],
                                        stdout=subprocess.PIPE)
                strres = result.stdout.decode('utf-8')
                self.wfile.write(bytes(strres, "utf-8"))
            else:
                self.wfile.write(bytes("Can't read host from config", 'utf-8'))
        except Exception as e:
            self.wfile.write(bytes(e, "utf-8"))
        return


def run():
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    httpd.serve_forever()


run()
