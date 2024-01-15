import socket, pickle, time
import Scripts.Car


class Client:

  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.latency = 0.0
    self.data: list[Scripts.Car.Car] = []
    self.send_data = None
    self.running = True
    self.connection_status = False
    self.client.settimeout(2)
  
  def connect(self, __address):
    try:
      self.client.connect(__address)
      self.connection_status = True
    except:
      self.connection_status = False
  
  def close(self):
    self.running = False
    self.client.close()
  
  def handle_data(self):
    while self.running:
      if self.connection_status:
        try:
          start_time = time.time()
          data = pickle.dumps(self.send_data)
          self.client.send(data)
          self.data = pickle.loads(self.client.recv(1024))
          end_time = time.time()
          self.latency = (end_time - start_time) * 1000
        except socket.timeout:
          pass
        except Exception as e:
          print(e)
          self.client.close()
          self.connection_status = False
          self.running = False