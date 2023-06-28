import pygame
from constantes import *
from pygame.locals import *
import random


class Personaje(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\nave\\nave-arriba-1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()

        self.velocidad = VELOCIDAD_PERSONAJE
        self.vida = VIDAS_PERSONAJE
        self.misil_disparado = False
        self.misil_mejorado_disparado = False
        self.contador_municion = MUNICION_PERSONAJE 
        self.contador_municion_mejorada = 0
        self.direccion_personaje_x = 0
        self.direccion_personaje_y = -1
        self.nombre_imagen_nave_actual = "nave-arriba-1.png"
        self.tamanio_bala_actual = (ALTO_MUNICION, ANCHO_MUNICION)


    def chequeo_teclas(self, grupo_balas, vida_personaje, grupo_balas_mejorada=None):
        """
        - Verifica si se presiona alguna tecla, si se presiona, hace algo.
        - Recibe la tecla que se presiona.
        - Retorna la imagen de la nave, segun a donde esta apuntando.
        """
        teclas_presionadas = pygame.key.get_pressed()
        self.vida_personaje = vida_personaje

        if teclas_presionadas[K_a]:
            self.rect.x -= self.velocidad
            self.caracteristicas_nave_y_bala(sentido="izquierda", dir_bala_x=-1, dir_bala_y=0, tamanio_bala=(ANCHO_MUNICION, ALTO_MUNICION), tamanio_nave=(ANCHO_PERSONAJE, ALTO_PERSONAJE))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas, grupo_balas_mejorada)

        if teclas_presionadas[K_d]:
            self.rect.x += self.velocidad
            self.caracteristicas_nave_y_bala(sentido="derecha", dir_bala_x=1, dir_bala_y=0, tamanio_bala=(ANCHO_MUNICION, ALTO_MUNICION), tamanio_nave=(ANCHO_PERSONAJE, ALTO_PERSONAJE))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas, grupo_balas_mejorada)

        if teclas_presionadas[K_w]:
            self.rect.y -= self.velocidad
            self.caracteristicas_nave_y_bala(sentido="arriba", dir_bala_x=0, dir_bala_y=-1, tamanio_bala=(ALTO_MUNICION, ANCHO_MUNICION), tamanio_nave=(ALTO_PERSONAJE, ANCHO_PERSONAJE))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True     
                self.chequeo_municion(grupo_balas, grupo_balas_mejorada)
        
        if teclas_presionadas[K_s]:
            self.rect.y += self.velocidad
            self.caracteristicas_nave_y_bala(sentido="abajo", dir_bala_x=0, dir_bala_y=1, tamanio_bala=(ALTO_MUNICION, ANCHO_MUNICION), tamanio_nave=(ALTO_PERSONAJE, ANCHO_PERSONAJE))

            if teclas_presionadas[K_SPACE] and not self.misil_disparado:
                self.misil_disparado = True
                self.chequeo_municion(grupo_balas, grupo_balas_mejorada)

        # Chequeo de disparo de misil normal
        if teclas_presionadas[K_SPACE] and not self.misil_disparado:
            self.misil_disparado = True
            self.nombre_bala = self.nombre_imagen_nave_actual
            self.tamanio_bala_actual = self.tamanio_bala 
            self.direccion_x_bala = self.direccion_personaje_x
            self.direccion_y_bala = self.direccion_personaje_y
            self.chequeo_municion(grupo_balas, grupo_balas_mejorada)

        if not teclas_presionadas[K_SPACE]:
            self.misil_disparado = False

        # Chequeo de disparo de misil mejorado
        if teclas_presionadas[K_v] and not self.misil_mejorado_disparado:
            self.misil_mejorado_disparado = True
            self.nombre_bala = self.nombre_imagen_nave_actual
            self.tamanio_bala_actual = self.tamanio_bala 
            self.direccion_x_bala = self.direccion_personaje_x
            self.direccion_y_bala = self.direccion_personaje_y
            self.chequeo_municion(grupo_balas, grupo_balas_mejorada, mejorada=True)
    
        if not teclas_presionadas[K_v]:
            self.misil_mejorado_disparado = False

        # Para que el personaje no pueda salir de la pantalla
        self.rect.x = max(0, min(self.rect.x, ANCHO_PANTALLA - self.rect.width))
        self.rect.y = max(ALTURA_MENU_SUPERIOR - 10, min(self.rect.y, ALTO_PANTALLA + 60 - self.rect.height))

        PANTALLA_JUEGO.blit(self.image, self.rect) # Dibuja la imagen del personaje


    def caracteristicas_nave_y_bala(self, sentido:str, dir_bala_x:int, dir_bala_y:int, tamanio_bala, tamanio_nave) -> None:
        """
        - Especifica los nombre de imagen, direcciones y demas al momento de moverse el personaje.
        - Recibe la posicion que tiene la nave en ese momento(donde esta apuntando), la direccion en x e y de la bala.
        - No retorna nada
        """
        if self.vida_personaje >= 3:
            self.image = pygame.image.load(RECURSOS + "personaje\\nave\\nave-{}-1.png".format(sentido)).convert_alpha()
        elif self.vida_personaje == 2:
            self.image = pygame.image.load(RECURSOS + "personaje\\nave\\nave-{}-2.png".format(sentido)).convert_alpha()
        elif self.vida_personaje == 1:
            self.image = pygame.image.load(RECURSOS + "personaje\\nave\\nave-{}-3.png".format(sentido)).convert_alpha()

        self.image = pygame.transform.scale(self.image, tamanio_nave)
        self.nombre_bala = "bala-{}.png".format(sentido)
        self.tamanio_bala = tamanio_bala
        self.direccion_x_bala = dir_bala_x
        self.direccion_y_bala = dir_bala_y
        self.direccion_personaje_x = self.direccion_x_bala
        self.direccion_personaje_y = self.direccion_y_bala
        self.nombre_imagen_nave_actual = self.nombre_bala
        self.tamanio_bala_actual = self.tamanio_bala


    def crear_bala(self, grupo_balas, grupo_balas_mejorada=None ,mejorada=False):
        """
        - Se encarga de crear la instancia de la bala del personaje.
        - Recibe el grupo de balas.
        - No retorna nada.
        """
        if mejorada:
            self.bala_mejorada = BalaPersonajeMejorada(self.rect.x, self.rect.y, self.direccion_x_bala, self.direccion_y_bala, self.nombre_bala, self.tamanio_bala)
            grupo_balas_mejorada.add(self.bala_mejorada)
        else:
            self.bala = BalaPersonaje(self.rect.x, self.rect.y, self.direccion_x_bala, self.direccion_y_bala, self.nombre_bala, self.tamanio_bala)
            grupo_balas.add(self.bala)

    
    def chequeo_municion(self, grupo_balas, grupo_balas_mejorada, mejorada=False):
        """-
        - Verifica si el personaje tiene municion, si tieneresta uno y llama a crer_bala().
        - Recibe el grupo de balas.
        - No retorna nada.
        """
        if mejorada:
            if self.contador_municion_mejorada > 0:
                self.contador_municion_mejorada -= 1
                self.crear_bala(grupo_balas, grupo_balas_mejorada, mejorada=True)
        else:
            if self.contador_municion > 0: 
                self.contador_municion -= 1
                self.crear_bala(grupo_balas)


class BalaPersonaje(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, nombre_bala, tamanio_bala) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\" + nombre_bala).convert_alpha()
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


class BalaPersonajeMejorada(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, nombre_bala, tamanio_bala) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\mejorada-" + nombre_bala).convert_alpha()
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
        self.image = pygame.image.load(RECURSOS + "personaje\\municion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(90, ANCHO_PANTALLA-70)
        self.rect.y = random.randint(90, ALTO_PANTALLA-70)
        
    def update(self) -> None:
        PANTALLA_JUEGO.blit(self.image, self.rect)


class BalaExtraMejorada(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(RECURSOS + "personaje\\municion-mejorada-extra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(90, ANCHO_PANTALLA-70)
        self.rect.y = random.randint(90, ALTO_PANTALLA-70)
        
    def update(self) -> None:
        PANTALLA_JUEGO.blit(self.image, self.rect)
    


    