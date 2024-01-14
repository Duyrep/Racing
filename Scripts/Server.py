import socket, threading, pickle, time


class Server:

  def __init__(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.clients: tuple[tuple[socket.socket, str]] = []
    self.data = None
    self.send_data = None
    self.running = True
  
  def bind(self, __address):
    self.server.bind(__address)
  
  def listen(self):
    self.server.listen()
  
  def host(self):
    self.bind(("localhost", 2024))
    self.listen()
    threading.Thread(target=self.handle_connection).start()
    threading.Thread(target=self.handle_data).start()
  
  def handle_connection(self):
    while self.running:
      try:
        conn, addr = self.server.accept()
        self.clients.append((conn, addr))
        print(addr)
      except:
        pass
  
  def handle_data(self):
    while True:
      try:
        print("a")
        for client in self.clients:
          data = pickle.loads(client[0].recv(1024))
          self.data = data
          print(data)
          client[0].send(pickle.dumps(self.send_data))
      except Exception as e:
        print(e)
      time.sleep(0.01)
        