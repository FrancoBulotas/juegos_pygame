import pygame
from constantes import *


class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_nave = pygame.image.load("Imagenes\\nave-arriba.png")
        self.imagen_nave = pygame.transform.scale(self.imagen_nave, (50, 100))
        self.rect_nave = self.imagen_nave.get_rect()
        self.vida = 3


