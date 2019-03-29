# Threading
import socket
import threading
import utils as u


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

        self._receive = receive

        # Start listener threads
        arduino_recv_thread = threading.Thread(target=self._receiver_arduino, args=(self._rpi_sock,))
        arduino_recv_thread.daemon = True
        arduino_recv_thread.start()

    def _receiver_android(self, sock):
        while True:
            data = sock.recv(1024)
            data = data.decode().strip()
            print('RECEIVED ANDROID', data)
            if not data:
                u.enable_print()
                print('RPi disconnected')

                try:
                    import winsound
                    frequency = 2500
                    duration = 1000
                    winsound.Beep(frequency, duration)
                except ImportError:
                    u.enable_print()
                    print('beep')
                    u.disable_print()

                break

            if data[0] == 'P':
                data = data.split('P')
                data[:] = [x for x in data if x != '']
                print(data)
                self._arduino_recv_queue.extend(data)

            if self._arduino_recv_queue:
                next_command = self._arduino_recv_queue.pop(0)
                self._receive(next_command)

    def _receiver_arduino(self, sock):
        while True:
            data = sock.recv(1024)
            data = data.decode().strip()
            print('RECEIVED ARDUINO', data)
            if not data:
                break

            if data[0] == 'P':
                data = data.split('P')
                data[:] = [x for x in data if x != '']
                print(data)
                self._arduino_recv_queue.extend(data)
            if self._arduino_recv_queue:
                if len(data[0]) < 3 and data[0] != 'D':
                    next_command = self._arduino_recv_queue.pop(0)
                    if next_command != 'D':
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

    def wait_arduino(self, msg_or_pattern, is_regex=False):
        print("WAITING", msg_or_pattern)
        while True:
            if self._arduino_recv_queue:
                next_command = self._arduino_recv_queue.pop(0)

                if not is_regex:
                    if next_command == msg_or_pattern:
                        print("WAITED ARDUINO", next_command)
                        break
                else:
                    print("WAITED ARDUINO", next_command)
                    return next_command

    def wait_rpi(self, msg):
        while True:
            if self._arduino_recv_queue:
                next_command = self._arduino_recv_queue.pop(0)

                if next_command == msg:
                    print("WAITED RPI", next_command)
                    break


def _send(sock, msg):
    print("SENDING", msg)
    sock.sendall(msg.encode())
