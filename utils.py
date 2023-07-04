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
def calcBezier(t, P0, P1, P2, P3):
    term1 = pow((1 - t),3) * P0
    term2 = 3 * t * pow((1 - t), 2) * P1
    term3 = 3  * pow(t, 2) * (1 - t) * P2
    term4 = pow(t, 3) * P3
    return term1 + term2 + term3 + term4

#Draw cubic Bezier Curve and Casteljau's algorithm
def cubicBezierCurve(positions, t1, t2, screen, cubicCurve):
    x = calcBezier(t2, positions[0].x, positions[1].x, positions[2].x, positions[3].x)
    y = calcBezier(t2, positions[0].y, positions[1].y, positions[2].y, positions[3].y)

    point = (x, y)

    a, b, c = [linearBezierCurve(positions[i], positions[i+1], t1, screen, purple) for i in range(3)]

    pygame.draw.line(screen, purple, (a.x, a.y), (b.x, b.y), 2)
    pygame.draw.line(screen, purple, (b.x, b.y), (c.x, c.y), 2)

    start = linearBezierCurve(a, b, t1, screen, green)
    end = linearBezierCurve(b, c, t1, screen, green)

    pygame.draw.line(screen, green, (start.x, start.y), (end.x, end.y), 2)

    if len(cubicCurve) > 2:
        pygame.draw.lines(screen, red, False,  cubicCurve, 4)

    cubicCurve.append(point)