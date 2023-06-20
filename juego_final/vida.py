import pygame
from constantes import *


class Vida(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_vida = pygame.image.load(RECURSOS + "personaje\\corazon.png")
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (10, 10))
        self.rect_vida = self.imagen_vida.get_rect()

    def update(self, personaje = None, indice = 0, vidas_misil = None, rect_misil = None) -> None:
        if personaje:
            self.rect_vida.x = (personaje.rect_nave.x + (indice * 15))
            self.rect_vida.y = personaje.rect_nave.y - 15
            PANTALLA_JUEGO.blit(self.imagen_vida, self.rect_vida)

        elif vidas_misil:
            self.rect_vida.x = (rect_misil.x + (indice * 15))
            self.rect_vida.y = rect_misil.y - 15
            PANTALLA_JUEGO.blit(self.imagen_vida, self.rect_vida)

    