import argparse
import zmq
import random
import time
import sys


parser = argparse.ArgumentParser('Server: <inst><startport>')
parser.add_argument('inst', type=int, help='Instance number')
parser.add_argument('port', type=int, help='PORT number')
args = parser.parse_args()

inst = args.inst
start_port = args.port

context = zmq.Context()

socket = context.socket(zmq.PUB)
bind_port = int("{0}{1}".format(inst, start_port))
socket.connect("tcp://localhost:{0}".format(bind_port))

publisher_id = random.randrange(0,9999)

while True:
    topic = random.randrange(1,10)
    messagedata = "server#%s" % publisher_id
    print("%s %s" % (topic, messagedata))
    socket.send_string("%d %s" % (topic, messagedata))
    time.sleep(1)