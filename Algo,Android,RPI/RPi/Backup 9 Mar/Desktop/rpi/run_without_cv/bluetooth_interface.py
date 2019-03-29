from bluetooth import *
from socket import timeout
import Queue

class BluetoothWrapper(object):
    def __init__(self,btport=3):
        self.server_socket = None
        self.client_socket = None
        self.queue = Queue.Queue()
        try:
            self.server_socket = BluetoothSocket(RFCOMM)
            self.server_socket.bind(("", btport))
            self.server_socket.listen(1)  # Listen for requests
            self.port = self.server_socket.getsockname()[1]
            #assign the UUID of the application; the UUID used here is UUID for an application
            #requiring Serial Port Services
            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            #advertise the application on the SDP server
            advertise_service(
                self.server_socket, "MDP-Server",
                service_id=uuid,
                service_classes=[uuid, SERIAL_PORT_CLASS],
                profiles=[SERIAL_PORT_PROFILE]
                )
            print("Listening for BT connections on RFCOMM channel %d..." % self.port)
        except Exception as e:
            print("\nError: %s" % str(e))

    def close_bt_socket(self):

        if self.client_socket:
            self.client_socket.close()
            # self.client_socket.shutdown(socket.SHUT_RDWR)
            print("Closing client socket")
        if self.server_socket:
            self.server_socket.close()
            # self.client_socket.shutdown(socket.SHUT_RDWR)
            print("Closing server socket")
        self.bt_is_connected = False

    def is_connected(self):
        return self.client_socket is not None

    def accept_connection(self,btport=4):

        # Creating the server socket and bind to port
        try:
            self.client_socket = None
            self.client_socket, client_address = self.server_socket.accept()
            print("Accepted BlueTooth Connection from ", client_address)
            return self.client_socket
        except Exception as e:
            print("\nError: %s" % str(e))

    def accept_connection_and_flush(self):
        conn = self.accept_connection()
        #no peek method makes this unnecessarily harder
        next_msg = None
        while(self.queue.empty() is False):
            try:
                if(next_msg is None):
                    next_msg = self.queue.get()
                print("Flushing BT Interface...")
                conn.sendall(next_msg.encode())
                next_msg = None
            except(timeout,BluetoothError):
                conn = self.accept_connection()
        self.client_socket = conn
        return conn


    #we delegate read jobs to the read thread
    #we also delegate flushing of the queue to the reader thread
    def write(self,msg):
        try:
            #if the queue is not empty there was a disconnect and the reader thread is flushing, enqueue this msg
            if(self.queue.empty() is False):
                self.queue.put(msg)
            else:
                self.client_socket.send(str(msg))
            return True
        except Exception:
            self.queue.put(msg)
            return False



