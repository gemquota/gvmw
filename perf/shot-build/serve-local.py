#!/usr/bin/env python3
"""Serve this VEPA test build locally with the headers it needs.

Usage:  python3 serve-local.py [port]     (default port 8000)
Then open http://127.0.0.1:<port>/ in Chrome or Edge.

The simulator uses SharedArrayBuffer, which browsers only allow on a
cross-origin-isolated page, so a plain file:// open or a bare static server
will not do; this adds the COOP/COEP headers.
"""
import http.server, os, sys

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

Handler.extensions_map.update({'.js': 'text/javascript', '.mjs': 'text/javascript', '.wasm': 'application/wasm'})

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f'VEPA test build on http://127.0.0.1:{port}/  (Ctrl+C to stop)')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
