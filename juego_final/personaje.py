import pygame
from constantes import *
from pygame.locals import *
import random


class Personaje(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-arriba.png")
        self.imagen_nave = pygame.transform.scale(self.imagen_nave, (50, 100))
        self.rect_nave = self.imagen_nave.get_rect()
        self.vida = VIDAS_PERSONAJE
        self.misil_disparado = False
        self.contador_municion = MUNICION_PERSONAJE 

    def chequeo_teclas(self, teclas_presionadas, grupo_balas):
        """
        - Verifica si se presiona alguna tecla, si se presiona, hace algo.
        - Recibe la tecla que se presiona.
        - Retorna la imagen de la nave, segun a donde esta apuntando.
        """
        if teclas_presionadas[K_a]:
            self.rect_nave.x -= VELOCIDAD_PERSONAJE
            #Vida.rect_vida.x = self.rect_nave.x
            self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-izquierda.png")
            self.imagen_nave = pygame.transform.scale(self.imagen_nave, (ANCHO_PERSONAJE, ALTO_PERSONAJE))
            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.nombre_bala = "bala-izquierda.png"
                self.tamanio_bala = (ANCHO_MUNICION, ALTO_MUNICION)
                self.direccion_x_bala = -1
                self.direccion_y_bala = 0
                self.chequeo_municion(grupo_balas)

        if teclas_presionadas[K_d]:
            self.rect_nave.x += VELOCIDAD_PERSONAJE
            #Vida.rect_vida.x = self.rect_nave.x
            self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-derecha.png")
            self.imagen_nave = pygame.transform.scale(self.imagen_nave, (ANCHO_PERSONAJE, ALTO_PERSONAJE))
            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.nombre_bala = "bala-derecha.png"
                self.tamanio_bala = (ANCHO_MUNICION, ALTO_MUNICION)
                self.direccion_x_bala = 1
                self.direccion_y_bala = 0
                self.chequeo_municion(grupo_balas)

        if teclas_presionadas[K_w]:
            self.rect_nave.y -= VELOCIDAD_PERSONAJE
            #Vida.rect_vida.y = self.rect_nave.y
            self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-arriba.png")
            self.imagen_nave = pygame.transform.scale(self.imagen_nave, (ALTO_PERSONAJE, ANCHO_PERSONAJE))
            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.nombre_bala = "bala-arriba.png"
                self.tamanio_bala = (ALTO_MUNICION, ANCHO_MUNICION)
                self.direccion_x_bala = 0
                self.direccion_y_bala = -1
                self.chequeo_municion(grupo_balas)
        
        if teclas_presionadas[K_s]:
            self.rect_nave.y += VELOCIDAD_PERSONAJE
            #Vida.rect_vida.y = self.rect_nave.y
            self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-abajo.png")
            self.imagen_nave = pygame.transform.scale(self.imagen_nave, (ALTO_PERSONAJE, ANCHO_PERSONAJE))
            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.nombre_bala = "bala-abajo.png"
                self.tamanio_bala = (ALTO_MUNICION, ANCHO_MUNICION)
                self.direccion_x_bala = 0
                self.direccion_y_bala = 1
                self.chequeo_municion(grupo_balas)
        
        if not teclas_presionadas[K_SPACE]:
            self.misil_disparado = False


    def update(self, grupo_balas):
        self.bala = BalaPersonaje(self.rect_nave.x, self.rect_nave.y, self.direccion_x_bala, self.direccion_y_bala, self.nombre_bala, self.tamanio_bala)
        grupo_balas.add(self.bala)
    
    
    def chequeo_municion(self, grupo_balas):
        if self.contador_municion > 0: 
            self.contador_municion -= 1
            self.update(grupo_balas)


class BalaPersonaje(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, nombre_bala, tamanio_bala) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\" + nombre_bala)
        self.image = pygame.transform.scale(self.image, tamanio_bala)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion_x = dir_x
        self.direccion_y = dir_y
        self.municion = MUNICION_PERSONAJE

    def update(self):
        self.rect.x += (self.direccion_x * (VELOCIDAD_PERSONAJE+5))
        self.rect.y += (self.direccion_y * (VELOCIDAD_PERSONAJE+5))

        if self.rect.x > ANCHO_PANTALLA or self.rect.x < 0 or self.rect.y > ALTO_PANTALLA or self.rect.y < 70:
            self.kill() # eliminamos el misil si sale de la pantalla

    
class BalaExtra(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\municion.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, ANCHO_PANTALLA-20)
        self.rect.y = random.randint(20, ALTO_PANTALLA-90)
        
    def update(self) -> None:
        PANTALLA_JUEGO.blit(self.image, self.rect)
    

class Vida(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_vida = pygame.image.load(RECURSOS + "personaje\\corazon.png")
        self.imagen_vida = pygame.transform.scale(self.imagen_vida, (10, 10))
        self.rect_vida = self.imagen_vida.get_rect()

    def update(self, personaje = None, indice = 0, vida_misil = None, rect_vida_misil = None, imagen_vida_misil = None, rect_misil = None) -> None:
        if personaje:
            self.rect_vida.x = (personaje.rect_nave.x + (indice * 15))
            self.rect_vida.y = personaje.rect_nave.y - 15
            PANTALLA_JUEGO.blit(self.imagen_vida, self.rect_vida)

        elif vida_misil:
            rect_vida_misil.x = (rect_misil.x + (indice * 15))
            rect_vida_misil.y = rect_misil.y - 15
            PANTALLA_JUEGO.blit(imagen_vida_misil, rect_vida_misil)

    
    