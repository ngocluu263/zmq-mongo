import argparse
import zmq


parser = argparse.ArgumentParser('Forwarder device: <inst><startport>')
parser.add_argument('inst', type=int, help='Instance number')
parser.add_argument('start_port', type=int, help='Starting PORT number')

args = parser.parse_args()

inst = args.inst
start_port = args.start_port


def main():
    try:
        context = zmq.Context(1)

        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        bind_port = int("{0}{1}".format(inst, start_port))
        frontend.bind("tcp://*:{0}".format(bind_port))
        frontend.setsockopt_string(zmq.SUBSCRIBE, "")

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:{0}".format(bind_port+1))

        zmq.device(zmq.FORWARDER, frontend, backend)
    except Exception as e:
        print(e)
        print("Forwarder device at port {0} has failed".format(bind_port))
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()