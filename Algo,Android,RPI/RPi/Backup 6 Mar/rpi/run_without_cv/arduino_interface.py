import os
import serial
import time
import Queue


class ArduinoWrapper():

    def __init__(self):
        if os.path.exists('/dev/ttyACM0') == True:
            self.ser = serial.Serial('/dev/ttyACM0', 115200)
            print("Listening to Arduino interface....")
        elif os.path.exists('/dev/ttyACM1') == True:
            self.ser = serial.Serial('/dev/ttyACM1', 115200)
            print("Listening to Arduino interface....")
        else:
           raise Exception("Arduino interface not detected...")

    def reconnect(self):
        while(1):
            try:
                if os.path.exists('/dev/ttyACM0') == True:
                    self.ser = serial.Serial('/dev/ttyACM0', 115200)
                    break
                if os.path.exists('/dev/ttyACM1') == True:
                    self.ser = serial.Serial('/dev/ttyACM1', 115200)
                    break
                time.sleep(1)
            except Exception:
                continue
        print("Arduino Reconnected...")
        return self.ser

    def write(self, msg):
        self.ser.write("{}\n".format(msg).encode('UTF-8')) #serial comms need to encode then can send

    def get_connection(self):
        return self.ser
