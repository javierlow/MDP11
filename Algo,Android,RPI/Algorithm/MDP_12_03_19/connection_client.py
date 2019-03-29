# Threading
import socket
import threading
from utils import *


class Sender:
    def __init__(self, receive):
        host = '192.168.11.11'
        rpi_port = 5111

        # Socket to listen for arduino responses
        self._rpi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._rpi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._rpi_sock.connect((host, rpi_port))

        # Queues
        self._arduino_recv_queue = []
        self._android_recv_queue = []
        self._rpi_recv_queue = []

        self._receive = receive

        # Start listener threads
        recv_thread = threading.Thread(target=self._receiver_main, args=(self._rpi_sock,))
        recv_thread.daemon = True
        recv_thread.start()

    def _receiver_main(self, sock):
        while True:
            data = sock.recv(1024)
            data = data.decode().strip()
            print('RECEIVED ', data)
            if not data:
                break

            if data[0] == 'P':
                data = data.split('P')
                data[:] = [x for x in data if x != '']
                disable_print()
                if len(data[0]) > 8 and data[0][0:8] == 'waypoint':
                    self._android_recv_queue.extend(data)
                elif data[0] not in ['ca', 'be', 'bf', 'st', 'w', 'a', 's', 'd']:
                    self._arduino_recv_queue.extend(data)
                elif data[0] in ['ca', 'be', 'bf', 'st', 'w', 'a', 's', 'd']:
                    self._android_recv_queue.extend(data)
                else:
                    self._rpi_recv_queue.extend(data)
            if self._android_recv_queue:
                next_command = self._android_recv_queue.pop(0)
                self._receive(next_command)

    def _receiver_rpi(self, sock):
        while True:
            data = sock.recv(1024)
            if not data:
                break

            if data[0] == 'P':
                data = data.split('P')
                data[:] = [x for x in data if x != '']
                print(data)
                self._arduino_recv_queue.extend(data)

    def send_android(self, msg):
        to_send = 'T%s' % msg
        _send(self._rpi_sock, to_send)

    def send_arduino(self, msg):
        to_send = 'A%s' % msg
        _send(self._rpi_sock, to_send)

    def send_rpi(self, msg):
        to_send = 'R%s' % msg
        _send(self._rpi_sock, to_send)

    def wait_arduino(self, msg_or_pattern, sensor_reading=False):
        print("WAITING", msg_or_pattern)
        while True:
            if self._arduino_recv_queue:
                next_command = self._arduino_recv_queue.pop(0)

                if not sensor_reading:
                    if next_command == msg_or_pattern:
                        print("WAITED ARDUINO", next_command)
                        break
                else:
                    print("WAITED ARDUINO", next_command)
                    return next_command

    def wait_rpi(self, msg):
        while True:
            if self._rpi_recv_queue:
                next_command = self._rpi_recv_queue.pop(0)

                if next_command == msg:
                    print("WAITED RPI", next_command)
                    break


def _send(sock, msg):
    print("SENDING", msg)
    sock.sendall(msg.encode())
