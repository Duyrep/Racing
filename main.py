from Scripts.Car import Car
import pygame as pg
import os


class Game:

  def __init__(self):
    pg.init()
    self.display = pg.display.set_mode((640, 480), pg.RESIZABLE)
    self.clock = pg.time.Clock()
    self.UPDATE_TIME = pg.USEREVENT + 1
    self.FULLSCREEN = False
    self.DEBUG = False
    self.running = True
    self.choose = 0
    self.set_caption({})
    self.cars = [
      Car((20, 20), "White", [50] * 2),
      Car((20, 20), "Blue", [50] * 2),
      Car((20, 20), "Green", [50] * 2)
    ]
    pg.time.set_timer(self.UPDATE_TIME, 1000)

  def check_event(self):
    for e in pg.event.get():
      if e.type == pg.QUIT:
        self.running = False
      elif e.type == self.UPDATE_TIME:
        self.slow_updates()
      elif e.type == pg.KEYDOWN:
        if e.key == pg.K_F11:
          if self.FULLSCREEN:
            self.FULLSCREEN = False
            self.display = pg.display.set_mode((640, 480), pg.RESIZABLE)
          else:
            self.FULLSCREEN = True
            self.display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        elif e.key == pg.K_F3:
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
    
  def draw(self):
    self.display.fill("white")
    for car in self.cars:
      self.display.blit(
        self.rot_center(car.image, car.degree),
        (car.position[0] * car.size[0] / 10, car.position[1] * car.size[1] / 10)
      )

  def update(self):
    self.clock.tick(60)
    for car in self.cars:
      car.update(pg.key.get_pressed())
    self.cars[self.choose].event(pg.key.get_pressed())
    for car in self.cars:
      car.size = [int((self.display.get_size()[0] + self.display.get_size()[1]) / 2) / 10] * 2
    pg.display.update()
  
  def slow_updates(self):
    self.set_caption(
      {
        "Fps": f"{self.clock.get_fps():.1f}",
        "Speed": f"{self.cars[self.choose].speed:.1f}",
        "Car" : self.cars[self.choose].color
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

if __name__ == "__main__":
  game = Game()
  game.run()
