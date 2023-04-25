import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
    #  Wait for next request from client
    # message = socket.recv()
    # print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)
    print("send")
    #  Send reply back to client
    data = {"a": "b"}
    socket.send_json(data, flags=zmq.constants.NOBLOCK)
