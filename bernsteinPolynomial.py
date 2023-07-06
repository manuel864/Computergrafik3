import pygame
from colors import *
from position import Position
from utils import *
from button import Button

def startGame():
    width = 800
    height = 800

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 60

    t1 = 0
    t2 = 0
    speed = 0.004

    controlPoints = [Position(100, 500), Position(300, 100), Position(500, 100), Position(700, 500)]
    curvePoints = []

    running = True

    while running:
        screen.fill(white)
        clock.tick(fps)
        pygame.display.set_caption("Bezier Curve")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT

        for i in range(len(controlPoints) - 1):
            pygame.draw.line(screen, grey, (controlPoints[i].x, controlPoints[i].y), 
                             (controlPoints[i + 1].x, controlPoints[i + 1].y), 1)

        cubicBezierCurve(controlPoints, t1, t2, screen, curvePoints)

        bernsteinPolynomial(t1, screen)

        controlPoints[0].point(screen, purple)
        controlPoints[1].point(screen, green)
        controlPoints[2].point(screen, red)
        controlPoints[3].point(screen, darkBlue)

        if t1 >= 1:
            t1 = 0
            t2 = 0
            curvePoints.clear()
        
        
        t1 += speed
        t2 += speed

        pygame.display.update()

    pygame.quit()