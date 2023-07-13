from typing import Any
import pygame
import random
from constantes import *
from vida import Vida


class NaveAlien(pygame.sprite.Sprite):
    def __init__(self, nivel_dos = False, nivel_tres = False) -> None:
        super().__init__()
        self.bala_violeta = nivel_dos
        self.bala_plateada = nivel_tres

        if nivel_dos:
            self.image = pygame.image.load(RECURSOS + "enemigos\\nave-alien-violeta.png").convert_alpha()
        if nivel_tres:
            self.image = pygame.image.load(RECURSOS + "enemigos\\nave-alien-plateado.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randint((ALTO_PANTALLA - 300), ALTO_PANTALLA - self.rect.height)
        self.velocidad_x = 1 * VELOCIDAD_NAVE_ALIEN
        self.velocidad_y = -1 * VELOCIDAD_NAVE_ALIEN

        self.colision = False
        self.vida = VIDAS_NAVE_ALIEN
        self.vidas_nave = pygame.sprite.Group()
        for i in range(self.vida):
            vida = Vida()
            self.vidas_nave.add(vida)

        
    def actualizar(self, sonidos):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        for i in range(self.vida):   
            self.vidas_nave.update(None, i, self.vidas_nave, self.rect)

        if self.rect.left < 0:
            self.velocidad_x *= -1

        if self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1

        if self.rect.top < 70:
            self.velocidad_y *= -1

        if self.rect.bottom > ALTO_PANTALLA:
            self.velocidad_y *= -1

        if self.vida == 0:
            sonidos.SONIDO_EXPLOSION_NAVE.play()    
            self.vida -= 1
    
        PANTALLA_JUEGO.blit(self.image, self.rect)
    
    def crear_bala(self, grupo_balas, personaje):
        """
        - Se encarga de crear la instancia de la bala del alien.
        - Recibe el grupo de balas.
        - No retorna nada.
        """
        if self.vida > 0:
            self.bala = Misil(bala_alien=True, bala_violeta=self.bala_violeta, bala_plateado=self.bala_plateada, alien_x=self.rect.x, alien_y=self.rect.y)
            self.bala.objetivo = personaje
            self.bala.vida = VIDAS_ALIEN
            grupo_balas.add(self.bala)


class Misil(pygame.sprite.Sprite):
    def __init__(self, bala_alien = False, bala_violeta=False, bala_plateado=False, alien_x = None, alien_y = None, nivel_dos=False):
        super().__init__()
        self.bala_alien = bala_alien
        self.nivel_dos = nivel_dos

        if bala_alien:
            if bala_violeta:
                self.image = pygame.image.load(RECURSOS + "enemigos\\alien-verde.png").convert_alpha()   
                self.image = pygame.transform.scale(self.image, (60, 45))
            if bala_plateado:
                self.image = pygame.image.load(RECURSOS + "enemigos\\alien-plateado.png")   .convert_alpha()
                self.image = pygame.transform.scale(self.image, (55, 50))
            self.rect = self.image.get_rect()
            self.rect.x = alien_x
            self.rect.y = alien_y
        elif self.nivel_dos:
            self.image = pygame.image.load(RECURSOS + "enemigos\\asteroide.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (140, 80))
            self.rect = self.image.get_rect() 
            self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
            self.rect.y = ALTO_PANTALLA
        else:
            self.image = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 80))
            # Horizontal
            self.imagen_derecha = pygame.image.load(RECURSOS + "enemigos\\cohete-derecha.png").convert_alpha()
            self.imagen_derecha = pygame.transform.scale(self.imagen_derecha, (80, 40))
            self.imagen_izquierda = pygame.image.load(RECURSOS + "enemigos\\cohete-izquierda.png").convert_alpha()
            self.imagen_izquierda = pygame.transform.scale(self.imagen_izquierda, (80, 40))        
            # Vertical
            self.imagen_abajo = pygame.image.load(RECURSOS + "enemigos\\cohete-abajo.png").convert_alpha()
            self.imagen_abajo = pygame.transform.scale(self.imagen_abajo, (40, 80))
            self.imagen_arriba = pygame.image.load(RECURSOS + "enemigos\\cohete-arriba.png").convert_alpha()
            self.imagen_arriba = pygame.transform.scale(self.imagen_arriba, (40, 80))
            self.rect = self.image.get_rect()        
            self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
            self.rect.y = random.randint((ALTO_PANTALLA - 300), ALTO_PANTALLA - self.rect.height)
        
        # self.rect_horizontal = self.imagen_derecha.get_rect()
        # self.rect_vertical = self.imagen_arriba.get_rect()
        self.objetivo = None
        self.velocidad_x = random.randint(-VELOCIDAD_MISIL, VELOCIDAD_MISIL)
        self.velocidad_y = random.randint(-VELOCIDAD_MISIL, VELOCIDAD_MISIL)
        self.colision = False
        self.vida = VIDA_MISIL
        self.vidas_misil = pygame.sprite.Group()
        if not self.nivel_dos:
            for i in range(self.vida):
                vida = Vida()
                self.vidas_misil.add(vida)

    def update(self, sonidos):
        if self.objetivo:
            # Para que siga al personaje
            direccion = pygame.math.Vector2(self.objetivo.rect.center) - pygame.math.Vector2(self.rect.center)
            try:    
                direccion = direccion.normalize()
            except ValueError:
                pass
            velocidad = direccion * (VELOCIDAD_MISIL - 1)
            self.rect.center += velocidad
        elif self.nivel_dos:
            self.rect.y -= 8
        else:
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

        for i in range(self.vida):   
            self.vidas_misil.update(None, i, self.vidas_misil, self.rect)

        if not self.nivel_dos:
            if not self.bala_alien:
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
        else:
            if self.rect.top < 70:
                self.kill()
        
        if self.vida <= 0:
            #sonidos.SONIDO_EXPLOSION_MISIL.play()
            sonidos.canal_impactos.play(sonidos.SONIDO_EXPLOSION_MISIL)
            self.kill()