import pygame
import random
from constantes import *


class Vida(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_vida = pygame.image.load(RECURSOS + "personaje\\corazon.png")
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (10, 10))
        self.rect_vida = self.imagen_vida.get_rect()

    def update(self, personaje = None, indice = 0, vidas_misil = None, rect_misil = None) -> None:
        if personaje:
            self.rect_vida.x = (personaje.rect.x + (indice * 15))
            self.rect_vida.y = personaje.rect.y - 15
            PANTALLA_JUEGO.blit(self.imagen_vida, self.rect_vida)

        elif vidas_misil:
            self.rect_vida.x = (rect_misil.x + (indice * 15))
            self.rect_vida.y = rect_misil.y - 15
            PANTALLA_JUEGO.blit(self.imagen_vida, self.rect_vida)


class VidaExtra(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\corazon-extra.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(90, ANCHO_PANTALLA-70)
        self.rect.y = random.randint(90, ALTO_PANTALLA-70)
        
    def update(self) -> None:
        PANTALLA_JUEGO.blit(self.image, self.rect)