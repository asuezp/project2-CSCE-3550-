import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import jwt
import datetime
import json
from key_helper import get_key
import sqlite3
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

hostName = "localhost"
serverPort = 8080

def int_to_base64(value):
    """Convert an integer to a Base64URL-encoded string"""
    value_hex = format(value, 'x')
    # Ensure even length
    if len(value_hex) % 2 == 1:
        value_hex = '0' + value_hex
    value_bytes = bytes.fromhex(value_hex)
    encoded = base64.urlsafe_b64encode(value_bytes).rstrip(b'=')
    return encoded.decode('utf-8')

class MyServer(BaseHTTPRequestHandler):
    def do_PUT(self):
        self.send_response(405)
        self.end_headers()
        return

    # ... (other methods like PATCH, DELETE, HEAD)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        if parsed_path.path == "/auth":
            expired = 'expired' in params
            private_key = get_key(expired)
            if private_key:
                # Mock authentication
                auth_data = {"user": "username"}
                token_payload = {
                    "user": "username",
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                if expired:
                    token_payload["exp"] = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
                encoded_jwt = jwt.encode(token_payload, private_key, algorithm="RS256")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(encoded_jwt, "utf-8"))
                return

            self.send_response(403)
            self.end_headers()
            return

        self.send_response(405)
        self.end_headers()
        return

    def do_GET(self):
        if self.path == "/.well-known/jwks.json":
            conn = sqlite3.connect('totally_not_my_privateKeys.db')
            c = conn.cursor()
            c.execute("SELECT key FROM keys WHERE exp > ?", (int(time.time()),))
            valid_keys = c.fetchall()
            conn.close()
            keys = []
            for key_data in valid_keys:
                private_key = serialization.load_pem_private_key(key_data[0], password=None, backend=default_backend())
                public_key = private_key.public_key()
                pem_public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo)
                keys.append({
                    "kty": "RSA",
                    "use": "sig",
                    "kid": str(len(keys)),
                    "e": int_to_base64(public_key.public_numbers().e),
                    "n": int_to_base64(public_key.public_numbers().n),
                    "x5c": [pem_public_key.decode('utf-8')]
                })
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"keys": keys}), "utf-8"))
            return

        self.send_response(405)
        self.end_headers()
        return

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()