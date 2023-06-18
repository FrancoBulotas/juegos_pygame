import pygame
from pygame.locals import *
from gui_widget import Widget
from constantes import *

class Graph(Widget):
    def __init__(self,master,x=0,y=0,w=200,h=50,color_background=C_GREEN,color_border=C_RED,image_background=None):
        super().__init__(master,x,y,w,h,color_background,color_border,None,None,None,None,None)
       
        self.surface_element = pygame.Rect(x,y,w,h)
        self.x0 = 0
        self.x1 = 100
        self.y0 = 0
        self.y1 = 100

        self.render()
        
    def render(self):
        super().render()
        pygame.draw.line(self.slave_surface,C_GREEN, (self.x0, self.y0), (self.x1, self.y1),2)

    def update(self,lista_eventos):
        self.render()

    

