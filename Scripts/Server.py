import socket, threading, pickle, time
import Scripts.Car


class Server:

  def __init__(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.clients: list[socket.socket] = []
    self.clients_address: list[str] = []
    self.data: list[Scripts.Car.Car] = []
    self.send_data: list[Scripts.Car.Car] = []
    self.running = True
    self.size = 40
  
  def bind(self, __address):
    self.server.bind(__address)
  
  def listen(self):
    self.server.listen()
  
  def close(self):
    self.running = False
    self.server.close()
  
  def host(self):
    self.bind(("localhost", 2024))
    self.listen()
    threading.Thread(target=self.handle_connection).start()
    threading.Thread(target=self.handle_data).start()
  
  def handle_connection(self):
    while self.running:
      try:
        conn, addr = self.server.accept()
        self.clients.append(conn)
        self.clients_address.append(addr)
        self.data.append(Scripts.Car.Car((20, 20), "White", [self.size] * 2))
        print(addr)
      except socket.timeout:
        pass
  
  def handle_data(self):
    while True:
      index = 0
      for client in self.clients:
        try:
          index += 1
          data = pickle.loads(client.recv(1024))
          if data == None:
            continue
          self.data[index] = data
          client.send(pickle.dumps(self.send_data))
        except socket.timeout:
          pass
        except Exception as e:
          print(e)
          self.clients_address.pop(self.clients.index(client))
          self.data.pop(self.clients.index(client) + 1)
          self.clients.remove(client)
          client.close()
      time.sleep(0.01)
        