import pygame
from colors import *
from position import Position

#Calculate linear Bezier Curve
def linearBezierCurve(p0, p1, t, screen, color):
    x = (1 - t) * p0.x + t * p1.x
    y = (1 - t) * p0.y + t * p1.y
    point = Position(x, y)

    pygame.draw.circle(screen, color, (point.x, point.y), 8)

    return point

#Calculate bezier Curve based on Bernstein polynomials
def calcBezier(t, p0, p1, p2, p3):
    B0 = pow((1 - t),3) * p0
    B1 = 3 * t * pow((1 - t), 2) * p1
    B2 = 3  * pow(t, 2) * (1 - t) * p2
    B3 = pow(t, 3) * p3
    return B0 + B1 + B2 + B3

#Draw cubic Bezier Curve and Casteljau's algorithm
def cubicBezierCurve(positions, t1, t2, screen, cubicCurve):

    #calculate x and y value of Bezier curve
    x = calcBezier(t2, positions[0].x, positions[1].x, positions[2].x, positions[3].x)
    y = calcBezier(t2, positions[0].y, positions[1].y, positions[2].y, positions[3].y)

    point = (x, y)

    #lineare interpolation of 3 Points for Casteljau Algorithm
    a, b, c = [linearBezierCurve(positions[i], positions[i+1], t1, screen, purple) for i in range(3)]

    #draw line inbetween the Points a,b and c
    pygame.draw.line(screen, purple, (a.x, a.y), (b.x, b.y), 2)
    pygame.draw.line(screen, purple, (b.x, b.y), (c.x, c.y), 2)

    # #lineare interpolation of 2 Points for Casteljau Algorithm
    d = linearBezierCurve(a, b, t1, screen, green)
    e = linearBezierCurve(b, c, t1, screen, green)

    #draw line inbetween the Points d and e
    pygame.draw.line(screen, green, (d.x, d.y), (e.x, e.y), 2)

    #lineare interpolation of 1 Point for Casteljau Algorithm (The Point represents the progression of the curve)
    linearBezierCurve(d, e, t1, screen, blue)

    #draw beziercurve
    if len(cubicCurve) > 1:
        pygame.draw.lines(screen, blue, False, cubicCurve, 4)

    cubicCurve.append(point)

#draw Bernstein Polynoms
def bernsteinPolynomial(t, screen):
    B0_y = pow((1 - t), 3) * 200
    B1_y = 3 * t * pow((1 - t), 2) * 200
    B2_y = 3 * pow(t, 2) * (1 - t) * 200
    B3_y =pow(t, 3) * 200

    pygame.draw.rect(screen, purple, pygame.Rect(350, 800-B0_y, 25, B0_y))
    pygame.draw.rect(screen, green, pygame.Rect(380, 800-B1_y, 25, B1_y))
    pygame.draw.rect(screen, red, pygame.Rect(410, 800-B2_y, 25, B2_y))
    pygame.draw.rect(screen, darkBlue, pygame.Rect(440, 800-B3_y, 25, B3_y))