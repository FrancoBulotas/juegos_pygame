import pygame
import random
from constantes import *
from personaje import Vida


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint((ALTO_PANTALLA - 300), ALTO_PANTALLA - self.rect.height)
        self.velocidad_x = random.randint(-VELOCIDAD_ENEMIGO, VELOCIDAD_ENEMIGO)
        self.velocidad_y = random.randint(-VELOCIDAD_ENEMIGO, VELOCIDAD_ENEMIGO)
        self.colision = False
        
        self.imagen_vida = pygame.image.load(RECURSOS + "enemigos\\corazon.png")
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (10, 10))
        self.rect_vida = self.imagen_vida.get_rect()
        self.vida = 2
        self.vidas_misil = pygame.sprite.Group()
        for i in range(self.vida):
            vida = Vida()
            self.vidas_misil.add(vida)

    def update(self, grupo_balas):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        for i in range(self.vida):   
            self.vidas_misil.update(None, i, self.vidas_misil, self.rect_vida, self.imagen_vida, self.rect)

        if self.rect.left < 0:
            self.velocidad_x *= -1
            self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-derecha.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1
            self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-izquierda.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.top < 70:
            self.velocidad_y *= -1
            self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-abajo.png")
            self.image = pygame.transform.scale(self.image, (40, 80))

        if self.rect.bottom > ALTO_PANTALLA:
            self.velocidad_y *= -1
            self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png")
            self.image = pygame.transform.scale(self.image, (40, 80))
        
        # Verifico si la bala del personaje le pega al misil
        for bala in grupo_balas:
            if self.rect.colliderect(bala.rect):
                self.vida -= 1

                for vida in self.vidas_misil:
                    vida.kill()
                    break

                bala.kill()
        #si se queda sin vida chau misil
        if self.vida <= 0:
            self.kill()