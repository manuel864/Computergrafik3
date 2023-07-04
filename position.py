import pygame

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 24)
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12

    def collidepoint(self, pos):
        return pow((self.x - pos[0]), 2) + pow((self.y - pos[1]), 2) < pow(self.radius, 2)

    def point(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, self.y), 12)