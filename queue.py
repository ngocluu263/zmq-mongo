import argparse
import zmq

parser = argparse.ArgumentParser('Forwarder device: <inst><startport>')
parser.add_argument('fport', type=int, help='Instance number')
parser.add_argument('bport', type=int, help='Starting PORT number')
args = parser.parse_args()

front_port = args.fport
back_port = args.bport


def main():
    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.XREP)
        frontend.bind("tcp://*:{0}".format(front_port))
        # Socket facing services
        backend = context.socket(zmq.XREQ)
        backend.bind("tcp://*:{0}".format(back_port))

        zmq.device(zmq.QUEUE, frontend, backend)
    except Exception as e:
        print(e)
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()