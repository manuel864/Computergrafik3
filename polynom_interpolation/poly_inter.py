import pygame
import numpy as np

from .ui_elements import Button , InputBox, TargetPoint
from .utils_poly import convert_to_numpy_polynomial,check_target_hits, vander,map_range
pygame.font.init()


def runge(x):
    return -1/(1+x*x)


class Polynome_Interpolation:
    def __init__(self) -> None:

        self.w = 800
        self.h = 800
        self.intervall_start_scale = 4
        self.intervall_end_scale = 4



        self.user_poly = None

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.font = pygame.font.Font(None, 24)
        self.color = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.num_ticks = 4
        self.x0 = map_range(0,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.w)
        self.y0 = map_range(0,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.h)
        self.points = []
        self.target_points = []
        self.start_point = None
        self.lines = []
        self.i = 0
        self.is_drawing = False
        self.is_finished = False

        self.clear_btn = Button(230,self.h-100,100,50,(200,200,200),'Clear',function=self.reset)
        self.solve_btn = Button(120,self.h-100,100,50,(200,200,200),'Solve',function=self.solve)
        self.draw_graph_btn = Button(10,self.h-100,100,50,(200,200,200),'Draw',function=self.start_graph_drawing)
        self.change_points_btn = Button(self.w-210,self.h-100,150,50,(200,200,200),'Change Points',function=self.set_target_points)
        self.coef_input =InputBox(10,self.h-40,200,30,self.font,is_only_number=False)
        self.points_input =InputBox(self.w-210,self.h-40,200,30,self.font)

        self.txt_surface_koe = self.font.render('Koeffizienten:', True, (0,0,0))





    def start_graph_drawing(self):
        if self.coef_input.text:
            self.reset()
            self.get_user_poly()
            check_target_hits(self.target_points,self.user_poly)
            self.is_drawing = True
    
    def set_target_points(self):
        self.reset()
        self.target_points = []
        try:
            num = int(self.points_input.text)
            if num > 1:
                self.num_ticks = num
        except Exception as e:
            print('Could not convert string to int')
        
        

    def draw_truth(self):
        last_point = None
        for x in np.arange(-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale, 0.01):
            y = runge(x)
 
            y = map_range(y,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.h)
            x = map_range(x,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.w)
            if y >=0 and y <800:
                if not last_point:
                    last_point = (x,y)
                else:
                    pygame.draw.aalines(self.screen, (100,100,100), False, [last_point,(x,y)],blend=100)
                    last_point = (x,y)
    
    
    def polynomial_interpolation(self):
        '''
        Funktion um die Interpolationsaufgabe zu lösen 
        '''
        self.start_point = None
        x = []
        y = []
        for p in self.target_points:
            x.append(p.x)
            y.append(p.y)

        vandermonde = vander(x)
        coefficients = np.linalg.solve(vandermonde, y)
        polynomial = np.poly1d(coefficients[::-1])
        self.user_poly = polynomial

    def solve(self):
        self.reset()
        self.polynomial_interpolation()
        check_target_hits(self.target_points,self.user_poly)
        self.is_drawing = True

    def get_user_poly(self):
        poly_string = self.coef_input.text
        self.user_poly = -convert_to_numpy_polynomial(poly_string)

    def create_target_point(self,x):
        intervall_x = map_range(x,0,self.w,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale)
        intervall_y = runge(intervall_x)
        y =  map_range(intervall_y,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.h)
        if 800 > y and y > 0:
            self.target_points.append(TargetPoint(x,y,intervall_x,intervall_y,5))

    def reset_target_points(self):
        for t in self.target_points:
            t.color = t.base_color
            t.is_hit = False

    def draw_target_points(self):
        for t in self.target_points:
            t.draw(self.screen)


    

    def reset(self):
        self.is_drawing = False
        self.is_finished = False
        self.reset_target_points()
        self.draw_screen()
        self.i = 0
        self.lines = []
        self.points = []
        self.start_point = None



    def create_graph_points(self):
        self.lines = []
        self.points = []
        for x in np.arange(-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale, 0.01):
            y = np.polyval(self.user_poly,x)
 
            y = map_range(y,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.h)
            x = map_range(x,-1.0*self.intervall_start_scale, 1.0*self.intervall_end_scale,0,self.w)

            self.points.append((x, y)) 
        self.start_point = self.points[0] 
        self.lines = [self.start_point]

    def draw_screen(self):
        #BACKGROUND

        self.screen.fill((255, 255, 255))  
        
        pygame.draw.line(self.screen, (255, 0, 0), (0, self.y0), (self.w, self.y0))  # X-axis
        pygame.draw.line(self.screen, (0, 255, 0), (self.x0, 0), (self.x0, self.h))  # Y-axis
        
        #LABELS  
        
        x_start = -1.0 * self.intervall_start_scale
        x_end = 1.0 * self.intervall_end_scale
        y_start = -1.0 * self.intervall_start_scale
        y_end = 1.0 * self.intervall_end_scale

        x_ticks = np.linspace(x_start, x_end, self.num_ticks)
        y_ticks = np.linspace(y_start, y_end, self.num_ticks)
        # X Achse
        x_tick_interval = self.w / (self.num_ticks - 1)
        for i, x in enumerate(x_ticks):
            x_pos = i * x_tick_interval 
            pygame.draw.line(self.screen, self.color, (x_pos, self.y0 - 5), (x_pos, self.y0 + 5))  # Tick mark
            label = self.font.render(str(round(x,2)), True, self.color)
            label_rect = label.get_rect(center=(x_pos, self.y0 + 20))
            if len(self.target_points) < self.num_ticks:
                self.create_target_point(x_pos)
            self.screen.blit(label, label_rect)
        # Y Achse
        y_tick_interval = self.h / (self.num_ticks - 1)
        for i, y in enumerate(y_ticks):
            y_pos = i * y_tick_interval 
            pygame.draw.line(self.screen, self.color, (self.x0 - 5, y_pos), (self.x0 + 5, y_pos))  # Tick mark
            label = self.font.render(str(-1*round(y,2)), True, self.color)
            label_rect = label.get_rect(center=(self.x0 - 30, y_pos))
            self.screen.blit(label, label_rect)
        self.draw_truth()
        
        

    def drawGraph(self):
        if not self.start_point:
            self.create_graph_points()
        if self.is_finished: 
            pygame.draw.aalines(self.screen, self.color, False, self.lines,blend=100)
            return
        if self.i < len(self.points)-1:
            self.lines.append(self.points[self.i+1])
            pygame.draw.aalines(self.screen, self.color, False, self.lines,blend=100)  
            
            for t in self.target_points:
                if self.points[self.i+1][0] >= t.pos_x-t.radius:
                    if t.is_hit:
                        t.color = (0,255,0)
                else:
                    break
            self.draw_target_points()
            self.i += 1
            pygame.display.update()
        else:
            self.is_finished = True
            self.is_drawing = False


    def mouse_over_target_point(self):
        mouse_pos = pygame.mouse.get_pos()
        for p in self.target_points:
            if p.check_mouse_inside(mouse_pos[0],mouse_pos[1]):
                text_surface = self.font.render(f'{round(p.x,3)} | {round(-p.y,3)}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(p.pos_x, p.pos_y - p.radius - 10))

                # Überprüfen, ob der Text abgeschnitten wird
                if text_rect.left < 0:
                    text_rect.left = 0
                elif text_rect.right > self.w:
                    text_rect.right = self.w
                if text_rect.top < 0:
                    text_rect.top = 0
                elif text_rect.bottom > self.h:
                    text_rect.bottom = self.h

                pygame.draw.rect(self.screen, (255, 255, 255), text_rect)  # Hintergrund für den Text
                self.screen.blit(text_surface, text_rect)

    def draw_text(self):
        
        self.screen.blit(self.txt_surface_koe, (220,self.h-45))
        txt_surface = self.font.render('x^n,x^n-1,..', True, (0,0,0))
        self.screen.blit(txt_surface, (220,self.h-25))

    def mainloop(self):
        '''
        Mainloop
        '''
        self.drawing = True
        while self.drawing:
            
            self.clock.tick(144)
            self.draw_screen()
            if not self.is_drawing:
                self.draw_target_points()
            self.mouse_over_target_point()
            self.clear_btn.draw(self.screen,self.font)
            self.solve_btn.draw(self.screen,self.font)
            self.draw_graph_btn.draw(self.screen,self.font)
            self.change_points_btn.draw(self.screen,self.font)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    self.drawing = False
                    return
                self.clear_btn.handle_event(e)
                self.solve_btn.handle_event(e)
                self.coef_input.handle_event(e)
                self.points_input.handle_event(e)
                self.change_points_btn.handle_event(e)
                self.draw_graph_btn.handle_event(e)
                


            self.coef_input.update()
            self.coef_input.draw(self.screen)
            self.points_input.update()
            self.points_input.draw(self.screen)
            if self.is_drawing or self.is_finished:
                self.drawGraph()
            self.draw_text()
            pygame.display.flip()

def main():
    pygame.display.set_caption('Polynominterpolation')
    game = Polynome_Interpolation()
    game.mainloop()
    
if __name__ == '__main__':
    main()
