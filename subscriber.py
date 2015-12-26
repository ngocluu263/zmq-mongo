import sys
import zmq
import pymongo


# def subscriber(port, data):
    # Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print("Collecting updates from server...")
# socket.connect ("tcp://localhost:{0}".format(port))
socket.connect ("tcp://localhost:{0}".format(19000))

topicfilter = "9"

socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

for update_nbr in range(10):
    string = socket.recv()
    topic, messagedata = string.split()
    print(topic, messagedata)


# if __name__ == "__main__":
#     print("Subscriber can't be launched directly!")