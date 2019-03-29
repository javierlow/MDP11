import socket
import time
import sys

class WiFi_conn(object):

        def __init__(self):
                self.tcp_ip = '192.168.11.11' # RPI IP address
                #self.tcp_ip = 'localhost'
                self.port = 5111
                self.conn = None
                self.client = None
                self.addr = None
                self.pc_is_connect = False

        def close_pc_socket(self):

                if self.conn:
                        self.conn.close()
                        print ("Closing server socket")
                if self.client:
                        self.client.close()
                        print ("Closing client socket")
                self.pc_is_connect = False

        def is_pc_connection(self):
                return self.pc_is_connect

        def send_message_PC(self, message):
                
                try:
                        self.client.sendto(message, self.addr)
                        print ("Sent to PC: %s" % message)

                except Exception as e:
                        print ("\nPC Write Error: %s " % str(e))
                        self.close_pc_socket()
                        self.initialise_connection()

        def initialise_connection(self):
                # Create a TCP/IP socket
                try:
                        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
                        self.conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        self.conn.bind((self.tcp_ip, self.port))
                        self.conn.listen(1)                                      
                        print ("Listening for incoming connections from PC...")
                        self.client, self.addr = self.conn.accept() 
                        print ("Connected! Connection address: ", self.addr)
                        self.pc_is_connect = True


                except Exception as e:   
                        print ("\nError: %s" % str(e))



        def receive_from_PC(self):

                try:
                        if self.client is None:
                                return  
                        pc_data = self.client.recv(512)
                        print ("Read from PC: %s" %pc_data)
                        return pc_data

                except Exception as e:
                        print ("\nPC Read Error: %s " % str(e))
                        self.close_pc_socket()
                        self.initialise_connection()


# Test wifi (Host) -- To test client use pc_test_socket.py

#        if __name__ == "__main__":
#                print ("main")
#                pc = WifiConnector()
#                pc.initialise_connection()
#                send_msg = ('Rpi Ready\n')
#                print ("send_message_PC(): %s " % send_msg)
#                pc.send_message_PC(send_msg)
#
#         while True:                
#
#                print ("read")
#                msg = pc.receive_from_PC()
#                print ("data received: %s " % msg)
#                pc.send_message_PC(send_msg)
#
#                print ("closing sockets")
#                pc.close_pc_socket()

