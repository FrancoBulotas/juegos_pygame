import pygame
from pygame.locals import *
from gui_widget import Widget
from constantes import *


class ProgressBar(Widget):
    def __init__(self,master,x=0,y=0,w=200,h=50,color_background=C_GREEN,color_border=C_RED,image_background=None,image_progress=None,value=1,value_max=5):
        super().__init__(master,x,y,w,h,color_background,color_border,image_background,None,None,None,None)
       
              
        self.surface_element = pygame.image.load(image_progress)
        self.surface_element = pygame.transform.scale(self.surface_element,(w/value_max, h)).convert_alpha()

        self.value=value
        self.value_max=value_max
        self.render()
        
    def render(self):
        super().render()
        for x in range(self.value):
            self.slave_surface.blit(self.surface_element, (x*self.w/self.value_max, 0))

    def update(self,lista_eventos):

        self.render()

    

