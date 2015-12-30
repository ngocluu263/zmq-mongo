import argparse
import zmq
import time
import sys
import random
import json
from pymongo import MongoClient
import logging


parser = argparse.ArgumentParser('Server: <back-queue port>')
# parser.add_argument('inst', type=int, help='Instance number')
parser.add_argument('port', type=int, help='PORT number')
args = parser.parse_args()

# inst = args.inst
port = args.port

context = zmq.Context()
socket = context.socket(zmq.REP)
# Connect to back-port of queue device
socket.connect("tcp://localhost:{0}".format(port))
# server_id = inst

# Establish connection to Mongo
HOST = "mongodb://localhost"
PORT = 27017
connection = MongoClient(HOST, PORT)
db = connection.djss
incometask = db.incometask
outcometask = db.outcometask

while True:
    # Wait for next request from client
    message = socket.recv_json()
    print("Received request")

    deserial = json.loads(message)

    print("Hash:", deserial['hash'])
    print("Passw:", deserial['password'])

    if deserial['opcode'] == 1:
        # Pass uploaded PDF to stego-processing
        reply = deserial['doc']

        incometask.insert_one({
                'payload': deserial['payload'],
                'password': deserial['password'],
                'doc': deserial['doc'],
                'timestamp': deserial['timestamp'],
                'hash': deserial['hash'],
                'opcode': deserial['opcode'],
        })

    elif deserial['opcode'] == 2:
        passw = deserial['password']
        incomehash = deserial['hash']
        reply = 'None'
        # Request for decode. Need to find record for this file and return payload
        cur = incometask.find_one({'password': passw, 'hash': incomehash})

        if cur is not None:
            reply = cur['payload']

    socket.send_string(reply)