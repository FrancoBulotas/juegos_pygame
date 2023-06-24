import pygame
from constantes import *

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        self.imagen_cerrar = pygame.image.load(RECURSOS + "menu\\cruz-negra.png")
        self.imagen_cerrar = pygame.transform.scale(self.imagen_cerrar, (50, 50))
        self.rect_cerrar = self.imagen_cerrar.get_rect()
        self.rect_cerrar.x = ANCHO_PANTALLA - 65
        self.rect_cerrar.y = 10

        for i, opcion in enumerate(opciones):
            x = 100 + (i * 250)
            y = ALTO_PANTALLA - 500 
            imagen = pygame.image.load(RECURSOS + "menu\\previsualizacion-nivel-{}.png".format(i + 1))
            self.opciones.append(Opcion(opcion, (x, y), imagen))

    def dibujar(self):
        PANTALLA_JUEGO.blit(self.imagen_cerrar, self.rect_cerrar)

        imagen_fondo_niveles =  pygame.image.load(RECURSOS + "menu\\fondo-menu-fin-1.png")
        imagen_fondo_niveles = pygame.transform.scale(imagen_fondo_niveles, (800, 400))
        PANTALLA_JUEGO.blit(imagen_fondo_niveles, (80, ALTO_PANTALLA - 600))


        fuente_titulo = pygame.font.SysFont("Arial Black", 120)
        texto_titulo = fuente_titulo.render("Space Survival", True, (0,0,0))
        PANTALLA_JUEGO.blit(texto_titulo, (80,40))

        fuente_niveles = pygame.font.SysFont("Arial Black", 50)
        texto_niveles = fuente_niveles.render("Niveles", True,(0,0,0))
        PANTALLA_JUEGO.blit(texto_niveles, (100, ALTO_PANTALLA - 600 ))

        for opcion in self.opciones:
            seleccionado = opcion is self.seleccion
            opcion.dibujar(seleccionado)

    def actualizar_seleccion(self, mouse_pos):
        if self.rect_cerrar.collidepoint(mouse_pos):
            self.seleccion = "salir"

        for opcion in self.opciones:
            if opcion.esta_seleccionado(mouse_pos):
                self.seleccion = opcion.texto
                

# Clase para representar una opción del menú
class Opcion:
    def __init__(self, texto, posicion, imagen):
        self.texto = texto
        self.posicion = posicion
        self.imagen = imagen
        self.imagen = pygame.transform.scale(self.imagen,(200,200))
        self.rect = pygame.Rect(posicion, (200, 220))

    def dibujar(self, seleccionado):
 
        PANTALLA_JUEGO.blit(self.imagen, self.posicion)

    def esta_seleccionado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
