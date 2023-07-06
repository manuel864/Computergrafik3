import pygame
import numpy as np

# Fenstergröße
WIDTH, HEIGHT = 800, 800
pygame.font.init()

import numpy as np

class Hermite_Point:
    def __init__(self,pos,tangent_point) -> None:
        self.pos = pos 
        self.tangent_point = tangent_point
        self.m = None
        self.update()
        self.base_color_circle = (128,128,128)
        self.base_color_tangete = (128,128,128)
        self.is_first = False
        self.is_sec = False
        self.dragging = False

        self.rect = pygame.Rect(self.pos[0]-20, self.pos[1]-20, 20, 20)

    def draw(self,screen):
        #Punkt
        if self.is_first:
            circle_color = (255,0,0)
        elif self.is_sec:
            circle_color = (0,255,0)
        else:
            circle_color = self.base_color_circle
        pygame.draw.circle(screen,circle_color,self.pos,10)
        #Tangente
        if self.is_first:
            tangente_color = (255,128,0)
        elif self.is_sec:
            tangente_color = (0,255,255)
        else:
            tangente_color = self.base_color_tangete
        end = self.pos + self.m
        pygame.draw.line(screen,tangente_color,self.pos,end)
        self.tangent_point.draw(screen,tangente_color)
        self.update()

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linke Maustaste gedrückt
                if self.rect.collidepoint(event.pos):  # Überprüfe, ob die Maus auf dem Viereck ist
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Linke Maustaste losgelassen
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:  # Wenn das Viereck gezogen wird, aktualisiere seine Position
                self.rect.x += event.rel[0]
                self.rect.y += event.rel[1]
        self.pos[0] = self.rect.x+10
        self.pos[1] = self.rect.y+10


    def update(self):
        self.m = self.tangent_point.pos-self.pos

class Tangente_point:
    def __init__(self,pos):
        self.pos = pos
        self.w = 16
        self.h = 16
        self.rect = pygame.Rect(self.pos[0]+4, self.pos[1]+4, 16, 16)
        self.dragging = False
    def draw(self,screen,color):
        pygame.draw.rect(screen,color,self.rect)

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linke Maustaste gedrückt
                if self.rect.collidepoint(event.pos):  # Überprüfe, ob die Maus auf dem Viereck ist
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Linke Maustaste losgelassen
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:  # Wenn das Viereck gezogen wird, aktualisiere seine Position
                self.rect.x += event.rel[0]
                self.rect.y += event.rel[1]
        self.pos[0] = self.rect.x+8
        self.pos[1] = self.rect.y+8

def hermite_interpolation(point0,point1, t,screen):

    p0 = point0.pos
    m0 = point0.m

    p1 = point1.pos
    m1 = point1.m

    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2

    p = h00 * p0 + h10  * m0 + h01 * p1 + h11  * m1


    font = pygame.font.Font(None, 19)
    lenght = 50
    #H00
    start = np.array((30,650))
    end = np.array((start[0],start[1]-lenght*h00))
    pygame.draw.line(screen,(172,172,172),(start[0],start[1]+lenght),(start[0],start[1]-lenght),width=10)
    pygame.draw.line(screen,(255,0,0),start,end,width=10)

    #H10
    start = np.array((50,650))
    end = np.array((start[0],start[1]-lenght*h10))
    pygame.draw.line(screen,(172,172,172),(start[0],start[1]+lenght),(start[0],start[1]-lenght),width=10)
    pygame.draw.line(screen,(255,128,0),start,end,width=10)

    #H01
    start = np.array((70,650))
    end = np.array((start[0],start[1]-lenght*h01))
    pygame.draw.line(screen,(172,172,172),(start[0],start[1]+lenght),(start[0],start[1]-lenght),width=10)
    pygame.draw.line(screen,(0,255,0),start,end,width=10)

    #H11
    start = np.array((90,650))
    end = np.array((start[0],start[1]-lenght*h11))
    pygame.draw.line(screen,(172,172,172),(start[0],start[1]+lenght),(start[0],start[1]-lenght),width=10)
    pygame.draw.line(screen,(0,255,255),start,end,width=10)
    
    
    pygame.draw.line(screen,(0,0,0),(25,650),(95,650))
    txt_surface = font.render('0', True, (0,0,0))
    screen.blit(txt_surface, (100, 640))

    pygame.draw.line(screen,(0,0,0),(25,650),(95,650))
    txt_surface = font.render('-1', True, (0,0,0))
    screen.blit(txt_surface, (100, 640+lenght))

    pygame.draw.line(screen,(0,0,0),(25,650),(95,650))
    txt_surface = font.render('1', True, (0,0,0))
    screen.blit(txt_surface, (100, 640-lenght))
    return p


def draw_graph(screen,lines):
    pygame.draw.lines(screen,(0,0,0),False,lines)

def draw_points(screen,points):
    for p in points:

        p.draw(screen)

def reset_point_color(points):
    for p in points:
        p.is_first = False
        p.is_sec = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    tangente_points = [Tangente_point(np.array((100,200))),
                       Tangente_point(np.array((200,200))),
                       Tangente_point(np.array((400,700)))
                       ]

    points = [Hermite_Point(np.array((100, 300)),tangente_points[0]),
              Hermite_Point(np.array((200, 100)),tangente_points[1]),
              Hermite_Point(np.array((500, 600)),tangente_points[2])]
    t = 0
    lines = [points[0].pos.copy()]
    num_of_splines = len(points)-1
    drawn_splines = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for t_p in tangente_points:
                t_p.handle_event(event)
            for h_p in points:
                h_p.handle_event(event)

        screen.fill((255,255,255))
        reset_point_color(points)
        if drawn_splines < num_of_splines:
            if t <= 1:
                p = hermite_interpolation(points[drawn_splines],points[drawn_splines+1],t,screen)
                lines.append(p)
                draw_graph(screen,lines)
                points[drawn_splines].is_first = True
                points[drawn_splines+1].is_sec = True
                t += 0.005
            else:
                t = 0.0
                drawn_splines +=1
        else:
            t = 0 
            drawn_splines = 0
            lines = [points[0].pos.copy()]
        draw_points(screen,points)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
