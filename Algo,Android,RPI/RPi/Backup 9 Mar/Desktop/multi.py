import sys
import time
import threading
import Queue
sys.path.append('/home/pi/.virtualenvs/cv/lib/python3.5/site-packages')
from wifi import *
from bluetooth_test2 import *
from sr import *
from camPi import *



class Main(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

                self.BT_thread = BT_conn()
                self.PC_thread = WiFi_conn()
                self.USB_thread = SR_conn()
                self.cam_thread = rpiCamera()

                # Initialize connections according to order below
                self.BT_thread.Connect_BT()
                self.PC_thread.initialise_connection()
                self.USB_thread.connect_USB()
                time.sleep(0.1)

       # RPI Functions 

        def send_cam(self, msg_to_cam):
                if msg_to_cam:
                        self.cam_thread.imageDetection(msg_to_cam)
                        print ("Message sent to [CAM]: %s" % msg_to_cam)
                        return True
                return False

        def receive_cam(self):

                while True:
                        read_cam_msg = self.cam_thread.send_from_cam()

                        if read_cam_msg:
                                if(read_cam_msg[0] == 'T'):
                                        self.send_to_bluetooth(read_cam_msg[1:])
                                        print ("\nMessage from [CAM] --> [ANDROID]: %s" % read_cam_msg [1:])
                                else:
                                        print ("Incorrect header from CAM: %s" %(read_cam_msg))

        # PC Functions 
        def send_to_PC(self, msg_to_pc):

                if self.PC_thread.is_pc_connection() and msg_to_pc:

                        self.PC_thread.send_message_PC(msg_to_pc)
                        print ("Message sent to [PC]: %s" % msg_to_pc)
                        return True
                return False

        def receive_message_PC(self):

                while True:
                        read_pc_msg = self.PC_thread.receive_from_PC()

                        if (self.PC_thread.is_pc_connection() and read_pc_msg):

                                pc_msg_list = read_pc_msg.decode('utf-8').split('\n')
                                print (pc_msg_list)
                                #pc_msg_list.pop()
                                print (pc_msg_list)
                                for pc_msg in pc_msg_list:

                                        if (pc_msg[0] == 'I'):
                                                self.send_cam(pc_msg[1:])
                                                print("\nMessage from [PC] --> [CAM]: %s" % pc_msg[1:])

                                        elif (pc_msg[0] == 'T'):
                                                print('checkpoint T')
                                                self.send_to_bluetooth((pc_msg[1:]).encode())
                                                print("\nMessage from [PC] --> [ANDROID]: %s" % pc_msg[1:])

                                        elif (pc_msg[0] == 'A'):
                                                print(pc_msg[1:])
                                                
                                                self.send_to_USB((pc_msg[1:]).encode())
                                                print("\nMessage from [PC] --> [ARDUINO]: %s" % pc_msg[1:])
                                        else:
                                                print("Incorrect header from PC: %s" % (pc_msg[1:]))



        # Android/BT functions 

        def send_to_bluetooth(self, msg_to_bt):

                if self.BT_thread.BT_connect() and msg_to_bt:
                        msg_to_bt_str = msg_to_bt.decode('ascii')
                        self.BT_thread.sendMess_BT(msg_to_bt_str)
                        print ("Message sent to [ANDROID]: %s" % msg_to_bt_str)
                        return True
                return False


        def receive_from_bluetooth(self):

                while True:

                        read_bt_msg = self.BT_thread.rcvMess_BT()

                        if self.BT_thread.BT_connect() and read_bt_msg :

                                # Android to PC, check first letter for destination
                                print (read_bt_msg[0])
                                if(read_bt_msg[0] == 'P'):

                                        read_bt_msg = read_bt_msg.decode('ascii').join('\r\n').encode()
                                        self.send_to_PC(read_bt_msg[2:])
                                        print ("\nMessage from [ANDROID] --> [PC]: %s" % read_bt_msg[1:])

                                # Android to Arduino, check first letter for destination
                                elif(read_bt_msg[0] == 'A'):

                                        self.send_to_USB(read_bt_msg[1:])
                                        print ("\nMessage from [ANDROID] --> [ARDUINO]: %s" % read_bt_msg[1:])
                                else:
                                        print ("Incorrect header [%s] from BT: %s" %(read_bt_msg[0] ,read_bt_msg))

        # Arduino Comm functions 

        def send_to_USB(self, msg_to_sr):

                if self.USB_thread.USB_is_connected() and msg_to_sr:
                        self.USB_thread.flush()
                        msg_to_sr_char = msg_to_sr.decode('ascii')
                        self.USB_thread.send_to_USB(msg_to_sr_char+"\n")
                        print ("Message sent to [ARDUINO]: %s" % msg_to_sr_char)
                        return True
                return False

        def read_from_USB(self):

                while True:
                        read_sr_msg = self.USB_thread.read_message_USB()
                        #read_sr_msg = read_sr_msg.decode('ascii',errors='ignore').strip('\r\r')
                        #read_sr_msg= read_sr_msg.encode('ascii')
                        if self.USB_thread.USB_is_connected() and read_sr_msg:
                                
                                #read_sr_msg.decode().encode('utf-8')
                                #if (read_sr_msg.decode('ascii')[1] != '\x0b'):
                                #read_sr_msg= read_sr_msg.decode('utf-8')

                                if(read_sr_msg[0] == 'P'):

                                        self.send_to_PC(read_sr_msg[1:])
                                        print ("\nMessage from [ARDUINO] --> [PC]: %s" % read_sr_msg[1:])

                                elif(read_sr_msg[0] == 'T'):
                                                
                                        self.send_to_bluetooth(read_sr_msg[1:])
                                        print ("\nMessage from [ARDUINO] --> [ANDROID]: %s" % read_sr_msg[1:])

                                else:
                                        print ("Incorrect header from SR: %s" % read_sr_msg)
                        else:
                                        continue

        def initialize_threads(self):

                # PC read and write thread
                read_from_PC_thread = threading.Thread(target = self.receive_message_PC, name = "pc_read_thread")
                write_to_PC_thread = threading.Thread(target = self.send_to_PC, args = ("",), name = "pc_write_thread")

                # Bluetooth (BT) read and write thread
                read_from_BT_thread = threading.Thread(target = self.receive_from_bluetooth, name = "bt_read_thread")
                write_to_BT_thread = threading.Thread(target = self.send_to_bluetooth, args = ("",), name = "bt_write_thread")

                # Serial (SR) read and write thread
                read_from_USB_thread = threading.Thread(target = self.read_from_USB, name = "sr_read_thread")
                write_to_USB_thread = threading.Thread(target = self.send_to_USB, args = ("",), name = "sr_write_thread")

                # RPI read/write thread
                read_cam_thread = threading.Thread(target = self.send_cam, args=("",), name = "cam_send_thread")
                write_cam_thread = threading.Thread(target = self.receive_cam, name = "cam_receive_thread")

                # Set threads as daemons
                read_from_PC_thread.daemon = True
                write_to_PC_thread.daemon = True
                read_from_BT_thread.daemon = True
                write_to_BT_thread.daemon = True
                read_from_USB_thread.daemon = True
                write_to_USB_thread.daemon = True
                read_cam_thread.daemon = True
                write_cam_thread.daemon = True

                # Start Threads
                read_from_PC_thread.start()
                write_to_PC_thread.start()
                read_from_BT_thread.start()
                write_to_BT_thread.start()
                read_from_USB_thread.start()
                write_to_USB_thread.start()
                read_cam_thread.start()
                write_cam_thread.start()

                print ("All threads initialized successfully")

        def close_all_sockets(self):
                self.PC_thread.close_pc_socket()
                self.BT_thread.close_bt()
                self.USB_thread.close_serial_socket()
                print ("End threads")

        def keep_main_alive(self):
                while True:
                        time.sleep(1)

if __name__ == "__main__":
        realRun = Main()
        realRun.initialize_threads()
        realRun.keep_main_alive()
        realRun.close_all_sockets()
