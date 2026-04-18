
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, threading, webbrowser, sys, subprocess, importlib

try:
    import chess
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "python-chess"])
    importlib.invalidate_caches()
    import chess

HOST = "127.0.0.1"
PORT = 8765

board = chess.Board()

class Handler(BaseHTTPRequestHandler):
    def _json(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path in ["/", "/chess.html"]:
            with open("chess.html", "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/state":
            self._json()
            self.wfile.write(json.dumps({"fen": board.fen(), "turn": "white" if board.turn else "black"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        data = json.loads(raw.decode()) if raw else {}

        if self.path == "/move":
            frm = data.get("from")
            to = data.get("to")
            if not frm or not to:
                self._json(400)
                self.wfile.write(json.dumps({"ok": False, "error": "missing fields"}).encode())
                return

            try:
                move = chess.Move.from_uci(frm + to)
            except:
                self._json(400)
                self.wfile.write(json.dumps({"ok": False, "error": "bad move"}).encode())
                return

            if move in board.legal_moves:
                board.push(move)
                self._json()
                self.wfile.write(json.dumps({"ok": True, "fen": board.fen()}).encode())
            else:
                self._json(400)
                self.wfile.write(json.dumps({"ok": False, "error": "illegal"}).encode())

        elif self.path == "/undo":
            if board.move_stack:
                board.pop()
            self._json()
            self.wfile.write(json.dumps({"ok": True, "fen": board.fen()}).encode())

        elif self.path == "/reset":
            board.reset()
            self._json()
            self.wfile.write(json.dumps({"ok": True, "fen": board.fen()}).encode())
