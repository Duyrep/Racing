import socket, pickle, time, threading


class Client:

  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.latency = 0.0
    self.data = None
    self.send_data = None
    self.running = True
    self.connection_status = False
  
  def connect(self, __address):
    try:
      self.client.connect(__address)
      self.connection_status = True
    except:
      self.connection_status = False
  
  def handle_data(self):
    while self.running and self.connection_status:
      try:
        start_time = time.time()
        self.client.send(pickle.dumps(self.data))
        self.send_data = pickle.loads(self.client.recv(1024))
        end_time = time.time()
        self.latency = (end_time - start_time) * 1000
      except Exception as e:
        print(e)
        self.client.close()
        self.connection_status = False
        self.running = False