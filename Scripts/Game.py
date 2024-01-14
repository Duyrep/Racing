from Scripts.Car import Car
from Scripts.Server import Server
from Scripts.Client import Client
import pygame as pg
import os, threading


class Game:

  def __init__(self):
    pg.init()
    self.display = pg.display.set_mode((700, 700))
    self.clock = pg.time.Clock()
    self.UPDATE_TIME = pg.USEREVENT + 1
    self.DEBUG = False
    self.running = True
    self.choose = 0
    self.size = 40
    self.page = "Menu"
    self.set_caption({})
    self.server = Server()
    self.client = Client()
    self.mode = "None"
    self.main_car = Car((20, 20), "White", [self.size] * 2)
    self.buttons = {
      "Menu": {
        "Play": pg.Rect(150, 150, 400, 100),
        "Setting": pg.Rect(150, 300, 400, 100),
        "Quit": pg.Rect(150, 450, 400, 100)
      },
      "Play": {
        "Single Player": pg.Rect(150, 150, 400, 100),
        "Multiplayer": pg.Rect(150, 300, 400, 100),
        "Back": pg.Rect(150, 450, 400, 100)
      },
      "Multiplayer": {
        "Host": pg.Rect(150, 150, 400, 100),
        "Join": pg.Rect(150, 300, 400, 100),
        "Back": pg.Rect(150, 450, 400, 100)
      }
    }
    self.cars = []
    pg.time.set_timer(self.UPDATE_TIME, 1000)

  def check_event(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:
        self.running = False
      elif e.type == self.UPDATE_TIME:
        self.slow_updates()
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_F3:
          if self.DEBUG:
            self.DEBUG = False
          else:
            self.DEBUG = True
        elif e.key == pg.K_q:
          self.choose -= 1
          if self.choose > 0:
            self.choose = len(self.cars)
        elif e.key == pg.K_e:
          self.choose += 1
          if self.choose > len(self.cars) - 1:
            self.choose = 0
      elif e.type == pg.MOUSEBUTTONDOWN:
        if self.page == "Menu":
          if self.buttons["Menu"]["Play"].collidepoint(pg.mouse.get_pos()):
            self.page = "Play"
          elif self.buttons["Menu"]["Setting"].collidepoint(pg.mouse.get_pos()):
            self.page = "Setting"
          elif self.buttons["Menu"]["Quit"].collidepoint(pg.mouse.get_pos()):
            self.running = False
        elif self.page == "Play":
          if self.buttons["Play"]["Single Player"].collidepoint(pg.mouse.get_pos()):
            self.page = "PlayGame"
            self.mode = "Single Player"
          elif self.buttons["Play"]["Multiplayer"].collidepoint(pg.mouse.get_pos()):
            self.page = "Multiplayer"
          elif self.buttons["Play"]["Back"].collidepoint(pg.mouse.get_pos()):
            self.page = "Menu"
        elif self.page == "Multiplayer":
          if self.buttons["Multiplayer"]["Host"].collidepoint(pg.mouse.get_pos()):
            self.server.host()
            self.mode = "MultiplayerServer"
            self.page = "PlayGame"
          elif self.buttons["Multiplayer"]["Join"].collidepoint(pg.mouse.get_pos()):
            self.page = "PlayGame"
            self.mode = "MultiplayerClient"
            threading.Thread(target=self.client.connect, args=(("localhost", 2024),)).start()
            threading.Thread(target=self.client.handle_data).start()
          elif self.buttons["Multiplayer"]["Back"].collidepoint(pg.mouse.get_pos()):
            self.page = "Menu"
    
  def draw(self):
    self.display.fill("red")
    if self.page == "Menu":
      self.draw_button("Menu")
    elif self.page == "Play":
      self.draw_button("Play")
    elif self.page == "Multiplayer":
      self.draw_button("Multiplayer")
    elif self.page == "PlayGame":
      self.display.blit(pg.transform.scale(pg.image.load("Assets/Images/Map.png"), self.display.get_size()), (0, 0))
      for car in self.cars:
        self.display.blit(
          self.rot_center(pg.transform.scale(car.image, car.size), car.degree),
          (car.position[0] * car.size[0] / 10, car.position[1] * car.size[1] / 10)
        )
        pg.draw.circle(self.display, "blue", (car.x * car.size[0] / 10 + car.size[1] / 2, car.y * car.size[0] / 10 + car.size[0] / 2), 5)
      self.display.blit(
        self.rot_center(pg.transform.scale(self.main_car.image, self.main_car.size), self.main_car.degree),
        (self.main_car.position[0] * self.main_car.size[0] / 10, self.main_car.position[1] * self.main_car.size[1] / 10)
      )

  def draw_button(self, button):
    font = pg.font.SysFont(None, 70)
    buttons = self.buttons[button]
    for k, v in buttons.items():
      surface = pg.Surface((400, 100))
      surface.fill("green" if v.collidepoint(pg.mouse.get_pos()) else "blue")
      pg.draw.rect(surface, "black", (0, 0, v.w, v.h), 4)
      text = font.render(k, True, "black")
      surface.blit(text, text.get_rect(center=surface.get_rect().center))
      self.display.blit(surface, (v.x, v.y))
  
  def update(self):
    self.clock.tick(60)
    if self.page == "PlayGame":
      self.main_car.update(pg.key.get_pressed())
      self.main_car.event(pg.key.get_pressed())
      for car in self.cars:
        car.size = [self.size] * 2
    elif self.page == "MultiplayerServer":
      self.client.send_data = self.cars
      self.cars = self.client.data
    elif self.page == "MultiplayerClient":
      self.client.send_data = [self.main_car]
    pg.display.update()
  
  def slow_updates(self):
    if self.mode == "MultiplayerServer":
      self.set_caption(
        {
          "Fps": f"{self.clock.get_fps():.1f}",
          "Clients": [client[1] for client in self.server.clients]
        } if self.DEBUG else {}
      )
    elif self.mode == "MultiplayerClient":
      self.set_caption(
        {
          "Fps": f"{self.clock.get_fps():.1f}",
          "Ping": f"{self.client.latency:.1f}",
          "Connection status": self.client.connection_status
        } if self.DEBUG else {}
      )
  
  def set_caption(self, title: dict):
    caption = "Racing"
    for k, v in title.items():
      caption += f" | {k}: {v}"
    pg.display.set_caption(caption)
  
  def rot_center(self, image, angle):
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
  
  def run(self):
    while self.running:
      self.check_event()
      self.draw()
      self.update()
    pg.quit()
    os._exit(1)
