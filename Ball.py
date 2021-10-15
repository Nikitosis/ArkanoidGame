import pygame
from random import randrange as rnd


class Ball:
    def __init__(self, radius, speed, positionX, positionY, color):
        self.radius = radius
        self.speed = speed
        self.width = int(self.radius * 2 ** 0.5)
        self.x = positionX
        self.y = positionY
        self.shape = pygame.Rect(positionX, positionY, self.width, self.width)
        self.dx = 1
        self.dy = -1
        self.color = color

    def move(self):
        self.shape.x += self.speed * self.dx
        self.shape.y += self.speed * self.dy