# Arduino - Serial python script

#from config import *

import time
import serial
import threading


class Arduinoser(object):

    # Initialisation of Arduino
    def __init__(self):
        self.port = '/dev/ttyACM0'
        self.baud_rate = 9600
        self.ser_connection = None
        self.arduino_is_connected = False

    # Start and create connection to serial port
    def connect_ser(self):
        try:
            self.ser_connection = serial.Serial(self.port, self.baud_rate)
            self.arduino_is_connected = True
            print("Serial link connection with Arduino success!!")
        except Exception as e:
            print("Serial connection error encountered: %s" % str(e))

    # Disconnect and close connection to serial port
    def disconnect_ser(self):
        try:
            self.ser_connection.close()
            self.arduino_is_connected = False
            print("Serial link is disconnected")
        except Exception as e:
            print("Error encountered: %s" % str(e))

    # Re-connect all connections (Arduino)
    def reconnect_ser(self):
        self.disconnect_ser()
        time.sleep(2)
        self.connect_ser()

    # Method to return if Arduino is connected
    def is_connected(self):
        return self.arduino_is_connected

    # Write to Arduino via serial link
    def write_ser(self, ser_message):
            try:
                ser_message = ser_message.encode("UTF-8")
                self.ser_connection.write(str(ser_message))
                print("Write Serial: %s" % ser_message)

            except Exception as e:
                print("Serial connection error. Can't write to Arduino")
                self.reconnect_ser()

    # Read from arduino
    def read_ser(self):
            try:
                ser_message_read = self.ser_connection.readline()
                ser_message_read = ser_message_read.decode("UTF-8")
                print("\nFrom Arduino: %s" % ser_message_read)
                return ser_message_read

            except AttributeError:
                print("Serial connection error. Can't read from Arduino")
                self.reconnect_ser()

    """ Testing thread reading and writing to and from - Arduino """

    # Write thread to Arduino
    def write_thread_ser(self):
        while True:
            try:
                ser_message = raw_input()
                self.ser_connection.write(str.encode(ser_message))
                print("Write to Arduino: %s" % ser_message)
            except AttributeError:
                print("Error encountered. No value written. Attempting to reconnect..")
                self.reconnect_ser()

    # Read thread to Arduino
    def read_thread_ser(self):
        while True:
            try:
                ser_message_read = self.ser_connection.readline()
                ser_message_read = ser_message_read.decode("UTF-8")
                print("Received message from Arduino: %s" % ser_message_read)
            except AttributeError:
                print("Error encountered. No value read. Attempting to reconnect..")
                self.reconnect_ser()

    # Maintain process
    def maintain_process(self):
        while True:
            time.sleep(1)


# Initialise Arduino - Serial testing
if __name__ == "__main__":
    sertest = Arduinoser()
    sertest.connect_ser()
    print("Serial connection is successful..")

    try:
        # create read and write threads for android
        ser_read = threading.Thread(target=sertest.read_thread_ser, args=(), name="btreadthread")
        ser_write = threading.Thread(target=sertest.write_thread_ser, args=(), name="btwritethread")

        # set thread as Daemons
        ser_read.daemon = True
        ser_write.daemon = True

        # start thread
        ser_read.start()
        ser_write.start()

        sertest.maintain_process()

    except KeyboardInterrupt:
        print("Disconnecting Serial connection.")
        sertest.disconnect_ser()
