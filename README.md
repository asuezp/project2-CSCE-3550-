# JWKS Server with SQLite Integration

This project is an implementation of a JWKS (JSON Web Key Set) server with SQLite database integration for storing and retrieving private keys. The server provides two endpoints: `/auth` for issuing JWT tokens and `/.well-known/jwks.json` for retrieving the JWKS response containing public keys.


## Installation

1. python database_setup.py
2. python server.py
http://localhost:8080/auth
http://localhost:8080/auth?expired
http://localhost:8080/.well-known/jwks.json



<img width="1244" alt="Screenshot 2024-03-24 at 10 19 12 PM" src="https://github.com/asuezp/project2-CSCE-3550-/assets/47001273/76520f7d-c8f0-44b6-83bd-56460d5fd1f5">
