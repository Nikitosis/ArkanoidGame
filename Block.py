import pygame


class Block():
    def __init__(self, x, y, width, height, color):
        self.shape = pygame.Rect(x, y, width, height)
        self.color = color
