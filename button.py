import pygame
from position import Position

class Button():
    def __init__(self, x, y, width, height, color, text='', textColor=(0,0,0), isClicked = False, isEnabled = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.textColor = textColor
        self.isEnabled = isEnabled
        self.isClicked = isClicked

    def draw(self, screen, font):
        button = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(screen, self.color, button, 0, 5)

        buttonText = font.render(self.text, True, self.textColor)

        screen.blit(buttonText, (self.x + (self.width - buttonText.get_width()) // 2, self.y + (self.height - buttonText.get_height()) // 2))

    def checkClick(self):
        if self.isEnabled == True:
            mouse_pos = pygame.mouse.get_pos()
            leftClick = pygame.mouse.get_pressed()[0]
            button = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
            if leftClick and button.collidepoint(mouse_pos):
                self.isClicked = True
                
            return self.isClicked