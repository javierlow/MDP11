import serial
import time

class SR_conn(object):
        def __init__(self):
                self.port = '/dev/ttyACM0'
                self.baud_rate = 115200
                self.service = None
                self.sr_is_connect = False

        def connect_USB(self):

                try:
                        self.service = serial.Serial(self.port, self.baud_rate)
                        self.sr_is_connect = True
                        print ("Serial link connected")

                except Exception as e:
                        print ("\nError (Serial): %s " % str(e))

        def USB_is_connected(self):
                return self.sr_is_connect

        def close_serial_socket(self):
                if (self.service):
                        self.service.close()
                        self.sr_is_connect = False 
                        print ("Closing serial socket")

        def send_to_USB(self, msg):

                try:
                        print(msg)
                        self.service.write(str(msg))
                        print ("Write to arduino: %s " % msg)

                except Exception as e:
                        print ("\nError Serial Write: %s " % str(e))
                        self.close_serial_socket()
                        time.sleep(2)
                        self.connect_USB()

        def read_message_USB(self):

                try:
                        received_data = self.service.readline()#.decode('ascii')#.strip('\r\r')
                        print ("Received from arduino: %s " % received_data)
                        return received_data

                except Exception as e:
                        print ("\nError Serial Read: %s " % str(e))
                        self.close_serial_socket()
                        time.sleep(2)
                        self.connect_USB()
        
        def flush(self):
                self.service.flushInput()
                self.service.flushOutput()
                
# Testing purpose

# if __name__ == "__main__":
#         print ("Running Main")
#         print (serial.__file__)
#         sr = USBConnector()
#         sr.connect_USB()
#         #print ("Serial connection Successful")

#         while True:  
#                 send_msg = input()
#                 print ("Writing [%s] to arduino" % send_msg)
#                 sr.send_to_USB(send_msg)

#                 print ("read")
#                 print ("Data received '%s' from Serial" % sr.read_message_USB())

#         print ("closing sockets")
#         sr.close_serial_socket()


