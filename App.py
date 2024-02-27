import uuid
import rsa
import jwt
from cryptography.hazmat.primitives import serialization
import rsa
import base64
import json
from flask import Flask, jsonify, request
import time

# Eric Tsuchiya
# CSCE 3550.002
# 02/25/2024
# Project 1 - JWKS server
# Please read the README and view the example screenshot within

app = Flask(__name__)

jwk_set = []

def int_to_base64url(val):
    # converting int to byte array
    num_bytes = (val.bit_length() + 7) // 8
    byte_array = val.to_bytes(num_bytes, byteorder='big')
    # encoding to base64
    b64 = base64.b64encode(byte_array)
    # encoding to base64url by replacing non url safe characters with url safe
    b64url = b64.replace(b'+', b'-').replace(b'/', b'_').replace(b'=', b'')
    # return as string
    return b64url.decode('utf-8')

# RSA key pair generation function
def generateKeyPair():
    public_key, private_key = rsa.newkeys(2048)
    global n
    global e

    n = public_key.n
    e = public_key.e
        
    # convert to PEM format
    global public_key_pem, private_key_pem
    public_key_pem = public_key.save_pkcs1("PEM").decode()
    private_key_pem = private_key.save_pkcs1("PEM").decode()

    # generate kid
    global kid
    kid = str(uuid.uuid4())

# Create JWK
def createJWK():
    n_b64 = int_to_base64url(n)
    e_b64 = int_to_base64url(e)
    
    # create JWK
    jwk = {
    'kty': "RSA",
    'use': "sig",
    'alg': "RS256",
    'kid': kid,
    'n': n_b64,
    'e': e_b64
    }

    # append the jwk to list
    jwk_set.append(jwk)

def createJWT(exp_time):
    # creates expiration time of JWT
    expiration = int(time.time()) + exp_time

    payload_data = {
    'exp': expiration,
    'kid': kid
    }

    # create jwt
    jwt_token = jwt.encode(payload_data, private_key_pem, algorithm='RS256', headers={'kid':kid})
    return jwt_token

@app.route("/.well-known/jwks.json", methods=["GET"])
def getJWKS():
    
    kid = request.args.get("kid")

    # return full JWKS if no kid specified
    if kid is None:
        jwks = {"keys": jwk_set}
        return jwks
    
    # if given a kid, search for jwk by kid and return
    for jwk in jwk_set:
        if jwk.get("kid") == kid:
            jwks = {"keys": jwk}
            return jwks

    # else return error
    return jsonify({"error": "JWK not found"}), 404
    

@app.route('/auth', methods=['POST'])
def auth():

    # default expire in an hour
    exp_time = 3600

    # if expired == true, set expired to an hour before
    args = request.args
    if 'expired' in args.keys():
        if args.get('expired') == "true":
            exp_time = -3600

    generateKeyPair()
    # no need to create JWK if expired
    if 'expired' in args.keys():
        if args.get('expired') != "true":
            createJWK()
    else:
        createJWK()
    
    jwt_token = createJWT(exp_time)
    return jwt_token

if __name__ == "__main__":
    app.run(port=8080)