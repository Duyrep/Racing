import pygame as pg
import math


class Car:

  def __init__(self, position: tuple, color: str | tuple, size):
    self.position = position
    self.color = color
    self.size = size
    self.x = position[0]
    self.y = position[1]
    self.image_path = f"Assets/Images/{color}Strip.png"
    self.braking = False
    self.speed = 0
    self.max_speed = 6
    self.min_speed = -4
    self.degree = 90
    self.acceleration = 0.1
    self.deceleration = 0.1
    self.swivel_speed = 0.5

  def move_straight(self):
    self.speed += self.acceleration
    if self.speed > self.max_speed:
      self.speed = self.max_speed

  def move_backwards(self):
    self.speed -= self.acceleration
    if self.speed > 0:
      self.speed -= self.deceleration
    if self.speed < self.min_speed:
      self.speed = self.min_speed

  def event(self, keys):
    self.braking = False
    if keys[pg.K_w] and not self.braking:
      self.move_straight()
    elif keys[pg.K_s] and not self.braking:
      self.move_backwards()
    if keys[pg.K_a] and self.speed != 0:
      self.degree += self.speed * self.swivel_speed
      if self.degree > 360:
        self.degree = 0
    if keys[pg.K_d] and self.speed != 0:
      self.degree -= self.speed * self.swivel_speed
      if self.degree < 0:
        self.degree = 360
    if keys[pg.K_SPACE]:
      self.braking = True
      
  def update(self, keys):
    if keys[pg.K_w] and not self.braking:
      pass
    elif keys[pg.K_s] and not self.braking:
      pass
    elif self.speed > 0:
      self.speed -= self.deceleration
      if self.braking:
        self.speed -= self.deceleration * 2
      if self.speed < 0:
        self.speed = 0
    elif self.speed < 0:
      self.speed += self.deceleration
      if self.braking:
        self.speed += self.deceleration * 2
      if self.speed > 0:
        self.speed = 0
    dx = math.cos(math.radians(self.degree)) * self.speed / 10
    dy = math.sin(math.radians(self.degree)) * self.speed / 10
    self.position = (self.position[0] + dx, self.position[1] - dy)
    self.x = self.position[0]
    self.y = self.position[1]
