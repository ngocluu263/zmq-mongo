import zmq
import sys
import random
import datetime
import json


def request(port, data):
    #data should be transformed by json.dumps
    context = zmq.Context()
    print("Connecting to server[{0}]...".format(port))
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:{0}".format(port))
    client_id = random.randrange(1,10005)

    # I send the data, received from django
    send_data = json.dumps(data)
    print("Sending data-request to server...")
    socket.send_json(send_data)

    # Now I wait for response from server
    message = socket.recv_json()

    return message


if __name__ == "__main__":
    data = {'date': 10000}
    request(10000, data)