import pygame


class Button:
    def __init__(self, x, y, width, height, color, text, textColor = (0,0,0),isEnabled = True ,function = None,*args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.textColor = textColor
        self.isEnabled = isEnabled
        self.function = function
        self.args = args


    def draw(self, screen, font):
        button = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(screen, self.color, button, 0, 5)

        buttonText = font.render(self.text, True, self.textColor)

        screen.blit(buttonText, (self.x + (self.width - buttonText.get_width()) // 2, self.y + (self.height - buttonText.get_height()) // 2))

    def handle_event(self,event):
        if self.isEnabled:
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                button = pygame.rect.Rect((self.x, self.y), (self.width, self.height))

                if button.collidepoint(mouse_pos):
                    if self.args:
                        self.function(self.args)
                    else:
                        self.function()
                
        
class InputBox:
    def __init__(self, x, y, w, h ,font,is_only_number=True,text=''):
        self.font = font
        self.COLOR_INACTIVE = (100,100,100)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = ''
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.COLOR_ACTIVE = (0,0,0)
        self.number_inputs = ['0','1','2','3','4','5','6','7','8','9']
        self.other_inputs = ['-','/','s','q','r','t','(',')',',','.']
        self.valid_inputs = self.number_inputs if is_only_number else  self.number_inputs+self.other_inputs


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in self.valid_inputs:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class TargetPoint:
    '''
    Pos_x, Pos_y : Position im Fenster 
    x,y : Position im Koordinaten System
    '''
    def __init__(self,pos_x,pos_y,x,y,radius) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = x 
        self.y = y
        self.radius = radius
        self.is_hit = False
        self.base_color = (255,0,0)
        self.hit_color = (0,255,0)
        self.color = self.base_color

    def check_mouse_inside(self,mouse_x,mouse_y):
        return abs(mouse_x - self.pos_x) <= self.radius and abs(mouse_y - self.pos_y) <= self.radius
    
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.pos_x,self.pos_y),5)