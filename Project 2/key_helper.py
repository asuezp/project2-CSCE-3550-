import sqlite3
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_key(expired=False):
    conn = sqlite3.connect('totally_not_my_privateKeys.db')
    c = conn.cursor()
    exp_condition = "<?" if expired else ">?"
    c.execute(f"SELECT key FROM keys WHERE exp {exp_condition} ORDER BY exp DESC LIMIT 1", (int(time.time()),))
    key_data = c.fetchone()
    conn.close()
    if key_data:
        private_key = serialization.load_pem_private_key(key_data[0], password=None, backend=default_backend())
        return private_key
    return None