import pygame
import random
from constantes import *


class Enemigos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes\\cohete-arriba.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint(0, ALTO_PANTALLA - self.rect.height)
        self.velocidad_x = random.randint(-7, 7)
        self.velocidad_y = random.randint(-7, 7)
        self.colision = False

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left < 0:
            self.velocidad_x *= -1
            self.image = pygame.image.load("Imagenes\\cohete-derecha.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1
            self.image = pygame.image.load("Imagenes\\cohete-izquierda.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.top < 0:
            self.velocidad_y *= -1
            self.image = pygame.image.load("Imagenes\\cohete-abajo.png")
            self.image = pygame.transform.scale(self.image, (40, 80))

        if self.rect.bottom > ALTO_PANTALLA:
            self.velocidad_y *= -1
            self.image = pygame.image.load("Imagenes\\cohete-arriba.png")
            self.image = pygame.transform.scale(self.image, (40, 80))