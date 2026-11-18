"""Local-only design preview. Serves theme assets and captured-page aliases."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path.startswith('/assets/'): file=ROOT/'theme'/path.lstrip('/')
        elif path in ['/preview.js','/reference-data.json','/heritage-home.html']: file=ROOT/'preview'/path.lstrip('/')
        elif '.' not in path.rsplit('/',1)[-1] or path.endswith('.html'): file=ROOT/'preview/index.html'
        else: self.send_error(404); return
        file=file.resolve()
        if not file.is_relative_to(ROOT) or not file.is_file(): self.send_error(404); return
        body=file.read_bytes();self.send_response(200);self.send_header('Content-Type',self.guess_type(str(file)));self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
if __name__=='__main__':
    print('Ammamma Shopify design preview: http://127.0.0.1:4180',flush=True)
    ThreadingHTTPServer(('127.0.0.1',4180),Handler).serve_forever()
