# UI library for python
import pygame

pygame.init()
pygame.font.init()


class ui:
    def __init__(self):
        self.timer = 0
        self.font = pygame.font.SysFont(None, 30)
        self.was_pressed = False
        self.buttons = {}

    def button(self, screen, x, y, width, height, text, color=(180, 180, 180), text_color=(0, 0, 0)):

        rect = pygame.Rect(x, y, width, height)


        pygame.draw.rect(screen, color, rect)


        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        self.buttons[(x, y)] = rect

    def textBox(self, screen, x, y, text, text_color=(255, 255, 255)):

        text_surface = self.font.render(text, True, text_color)
        screen.blit(text_surface, (x, y))

    def onclick(self, x, y):
        """
        Returns True if the mouse clicked the button

        ui.button(screen,100,100,100,50,"Click")
        if ui.onclick(100,100):
            print("Clicked")
        """

        if (x, y) not in self.buttons:
            return False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not self.was_pressed:
            self.was_pressed = True
            return self.buttons[(x,y)].collidepoint(mouse_pos) and mouse_pressed
        if not mouse_pressed:
            self.was_pressed = False

        #return self.buttons[(x, y)].collidepoint(mouse_pos) and mouse_pressed