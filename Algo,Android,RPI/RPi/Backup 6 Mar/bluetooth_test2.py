import subprocess
from bluetooth import *

class BT_Connector(object):
  
  def __init__(self):
	
      self.server_sock = None
      self.client_sock = None
      self.BT_connectt= False
      print("check1")
  
  def close_bt(self):
    if self.client_sock:
      self.client_sock.close()
      print("Closing client socket")
    if self.server_sock:
      self.server_sock.close()
      print("Closing server socket")
    self.BT_connectt = False

  def BT_connect(self):
    return self.BT_connectt
  
  def Connect_BT(self):
    #Creating the server socket and bind to port
    try:
      	self.server_sock = BluetoothSocket(RFCOMM)
	print("check2")
      	self.server_sock.bind(("", 3))
	print("check3")
      	self.server_sock.listen(1)
      	self.port = self.server_sock.getsockname()[1]
      	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
      
      	advertise_service(self.server_sock, "MDP-Server",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  # protocols = [ OBEX_UUID ]
                  )

      	print("Waiting for connection on RFCOMM channel %d" % self.port)
      #accept requests
      	self.client_sock, self.client_info = self.server_sock.accept()
        self.BT_connectt = True
      	print("Accepted connection from ", self.client_info)
      
    except Exception as e:
      	print ("\nError: %s" %str(e))

  def sendMess_BT(self,message):
    try:
      self.client_sock.send(str(message))

    except BluetoothError:
      print ("\nBluetooth Write Error. Connection lost")
      self.close_bt()
      self.Connect_BT()  
  
  def rcvMess_BT(self):
    try:
            data = self.client_sock.recv(1024)
            print("Received [%s]" % data)
            return data
            #client_sock.send(data + " i am pi!")
    except BluetoothError:
      print("disconnected")
      self.close_bt()
      self.Connect_BT()
      

#client_sock.close()
#server_sock.close()
#print("all done")
