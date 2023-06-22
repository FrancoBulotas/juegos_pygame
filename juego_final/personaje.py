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
        self.direccion_personaje_x = 0
        self.direccion_personaje_y = -1
        self.nombre_imagen_nave_actual = "nave-arriba.png"
        self.tamanio_bala_actual = (ALTO_MUNICION, ANCHO_MUNICION)


    def chequeo_teclas(self, grupo_balas):
        """
        - Verifica si se presiona alguna tecla, si se presiona, hace algo.
        - Recibe la tecla que se presiona.
        - Retorna la imagen de la nave, segun a donde esta apuntando.
        """
        teclas_presionadas = pygame.key.get_pressed()

        if teclas_presionadas[K_a]:
            self.rect_nave.x -= VELOCIDAD_PERSONAJE
            self.caracteristicas_nave_y_bala(posicion_nave_bala="izquierda", dir_bala_x=-1, dir_bala_y=0, tamanio_bala=(ANCHO_MUNICION, ALTO_MUNICION))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas)

        if teclas_presionadas[K_d]:
            self.rect_nave.x += VELOCIDAD_PERSONAJE
            self.caracteristicas_nave_y_bala(posicion_nave_bala="derecha", dir_bala_x=1, dir_bala_y=0, tamanio_bala=(ANCHO_MUNICION, ALTO_MUNICION))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas)

        if teclas_presionadas[K_w]:
            self.rect_nave.y -= VELOCIDAD_PERSONAJE
            self.caracteristicas_nave_y_bala(posicion_nave_bala="arriba", dir_bala_x=0, dir_bala_y=-1, tamanio_bala=(ALTO_MUNICION, ANCHO_MUNICION))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True     
                self.chequeo_municion(grupo_balas)
        
        if teclas_presionadas[K_s]:
            self.rect_nave.y += VELOCIDAD_PERSONAJE
            self.caracteristicas_nave_y_bala(posicion_nave_bala="abajo", dir_bala_x=0, dir_bala_y=1, tamanio_bala=(ALTO_MUNICION, ANCHO_MUNICION))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas)


        if teclas_presionadas[K_SPACE] and not self.misil_disparado:
            self.misil_disparado = True
            self.nombre_bala = self.nombre_imagen_nave_actual
            self.tamanio_bala_actual = self.tamanio_bala 
            self.direccion_x_bala = self.direccion_personaje_x
            self.direccion_y_bala = self.direccion_personaje_y
            self.chequeo_municion(grupo_balas)
        
        if not teclas_presionadas[K_SPACE]:
            self.misil_disparado = False

        # Para que el personaje no pueda salir de la pantalla
        self.rect_nave.x = max(0, min(self.rect_nave.x, ANCHO_PANTALLA - self.rect_nave.width))
        self.rect_nave.y = max(ALTURA_MENU_SUPERIOR - 10, min(self.rect_nave.y, ALTO_PANTALLA + 60 - self.rect_nave.height))

    def caracteristicas_nave_y_bala(self, posicion_nave_bala:str, dir_bala_x:int, dir_bala_y:int, tamanio_bala) -> None:
        """
        - Especifica los nombre de imagen, direcciones y demas al momento de moverse el personaje.
        - Recibe la posicion que tiene la nave en ese momento(donde esta apuntando), la direccion en x e y de la bala.
        - No retorna nada
        """
        self.imagen_nave = pygame.image.load(RECURSOS + "personaje\\nave-{}.png".format(posicion_nave_bala))
        self.nombre_bala = "bala-{}.png".format(posicion_nave_bala)
        self.tamanio_bala = tamanio_bala
        self.direccion_x_bala = dir_bala_x
        self.direccion_y_bala = dir_bala_y
        self.direccion_personaje_x = self.direccion_x_bala
        self.direccion_personaje_y = self.direccion_y_bala
        self.nombre_imagen_nave_actual = self.nombre_bala
        self.tamanio_bala_actual = self.tamanio_bala


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
    


    