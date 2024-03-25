import sqlite3
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Create/open the SQLite database
try:
    conn = sqlite3.connect('totally_not_my_privateKeys.db')
except sqlite3.OperationalError:
    # Database file doesn't exist, create a new one
    conn = sqlite3.connect('totally_not_my_privateKeys.db')

c = conn.cursor()

# Create the keys table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS keys
              (kid INTEGER PRIMARY KEY AUTOINCREMENT, key BLOB NOT NULL, exp INTEGER NOT NULL)''')

# Generate and store some example keys
private_key_1 = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
private_key_2 = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

pem_key_1 = private_key_1.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                        encryption_algorithm=serialization.NoEncryption())
pem_key_2 = private_key_2.private_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                        encryption_algorithm=serialization.NoEncryption())

# Store key 1 with expiry in 1 hour, key 2 with expiry now
c.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key_1, int(time.time() + 3600)))
c.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key_2, int(time.time())))
conn.commit()
conn.close()