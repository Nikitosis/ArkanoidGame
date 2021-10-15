import pygame

class Paddle:
    def __init__(self, positionX, positionY, width, height, speed, color):
        self.width = width
        self.height = height
        self.speed = speed
        self.shape = pygame.Rect(positionX, positionY, width, height)
        self.color = color

    def moveLeft(self):
        self.shape.left -= self.speed

    def moveRight(self):
        self.shape.right += self.speed