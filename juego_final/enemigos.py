import pygame
import random
from constantes import *
from vida import Vida


class Misil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        # Horizontal
        self.imagen_derecha = pygame.image.load(RECURSOS + "enemigos\\cohete-derecha.png")
        self.imagen_derecha = pygame.transform.scale(self.imagen_derecha, (80, 40))
        self.imagen_izquierda = pygame.image.load(RECURSOS + "enemigos\\cohete-izquierda.png")
        self.imagen_izquierda = pygame.transform.scale(self.imagen_izquierda, (80, 40))
        self.rect_horizontal = self.imagen_derecha.get_rect()
        # Vertical
        self.imagen_abajo = pygame.image.load(RECURSOS + "enemigos\\cohete-abajo.png")
        self.imagen_abajo = pygame.transform.scale(self.imagen_abajo, (40, 80))
        self.imagen_arriba = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png")
        self.imagen_arriba = pygame.transform.scale(self.imagen_arriba, (40, 80))
        self.rect_vertical = self.imagen_arriba.get_rect()

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint((ALTO_PANTALLA - 300), ALTO_PANTALLA - self.rect.height)
        #self.mask = pygame.mask.from_surface(self.image)

        self.velocidad_x = random.randint(-VELOCIDAD_ENEMIGO, VELOCIDAD_ENEMIGO)
        self.velocidad_y = random.randint(-VELOCIDAD_ENEMIGO, VELOCIDAD_ENEMIGO)
        self.colision = False
        self.vida = VIDA_ENEMIGO
        self.vidas_misil = pygame.sprite.Group()
        for i in range(self.vida):
            vida = Vida()
            self.vidas_misil.add(vida)

    def update(self, grupo_balas):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        for i in range(self.vida):   
            self.vidas_misil.update(None, i, self.vidas_misil, self.rect)

        if self.rect.left < 0:
            self.velocidad_x *= -1
            self.image = self.imagen_derecha

        if self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1
            self.image = self.imagen_izquierda

        if self.rect.top < 70:
            self.velocidad_y *= -1
            self.image = self.imagen_abajo

        if self.rect.bottom > ALTO_PANTALLA:
            self.velocidad_y *= -1
            self.image = self.imagen_arriba
        
        # # Verifico si la bala del personaje le pega al misil
        # for bala in grupo_balas:
        #     #if pygame.sprite.collide_mask(bala, self.mask):
        #     if bala.rect.colliderect(self.rect): 
        #         self.vida -= 1

        #         for vida in self.vidas_misil: # Eliminamos la imagen de la vida del misil al que el personaje impacta con sus balas
        #             vida.kill()
        #             break

        #         bala.kill()
        #si se queda sin vida chau misil
        if self.vida <= 0:
            self.kill()