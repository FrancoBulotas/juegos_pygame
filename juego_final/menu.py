import pygame
from constantes import *

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        self.imagen_cerrar = pygame.image.load(RECURSOS + "menu\\iconos\\cruz-roja.png")
        self.imagen_cerrar = pygame.transform.scale(self.imagen_cerrar, (50, 50))
        self.rect_cerrar = self.imagen_cerrar.get_rect()
        self.rect_cerrar.x = ANCHO_PANTALLA - 65
        self.rect_cerrar.y = 10

        for i, opcion in enumerate(opciones):
            x = 100 + (i * 350)
            y = ALTO_PANTALLA - 500 
            imagen = pygame.image.load(RECURSOS + "menu\\previsualizacion-nivel-{}.png".format(i + 1))
            self.opciones.append(Opcion(opcion, (x, y), imagen))

    def dibujar(self):
        PANTALLA_JUEGO.blit(self.imagen_cerrar, self.rect_cerrar)

        fuente_titulo = pygame.font.SysFont("Txt_IV25", 120)
        texto_titulo = fuente_titulo.render("Space Survival", True, (0,0,0))
        PANTALLA_JUEGO.blit(texto_titulo, (80,40))

        fuente_niveles = pygame.font.SysFont("Txt_IV25", 50)
        texto_niveles = fuente_niveles.render("Select Level", True,(0,0,0))
        PANTALLA_JUEGO.blit(texto_niveles, (120, ALTO_PANTALLA - 600 ))

        for opcion in self.opciones:
            opcion.dibujar()

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
        self.imagen = pygame.transform.scale(self.imagen,(300,380))
        self.rect = pygame.Rect(posicion, (300, 380))

    def dibujar(self):
        PANTALLA_JUEGO.blit(self.imagen, self.posicion)

    def esta_seleccionado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
