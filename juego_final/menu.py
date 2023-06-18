import pygame
from constantes import *

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        
        for i, opcion in enumerate(opciones):
            x = 100 + (i * 250)
            y = ALTO_PANTALLA - 500 
            imagen = pygame.image.load("Imagenes\\previsualizacion-nivel-{}.png".format(i + 1))
            self.opciones.append(Opcion(opcion, (x, y), imagen))

    def dibujar(self):
        for opcion in self.opciones:
            seleccionado = opcion is self.seleccion
            opcion.dibujar(seleccionado)

    def actualizar_seleccion(self, mouse_pos):
        for opcion in self.opciones:
            if opcion.esta_seleccionado(mouse_pos):
                self.seleccion = opcion
                

# Clase para representar una opción del menú
class Opcion:
    def __init__(self, texto, posicion, imagen):
        self.texto = texto
        self.posicion = posicion
        self.imagen = imagen
        self.imagen = pygame.transform.scale(self.imagen,(200,200))
        self.rect = pygame.Rect(posicion, (200, 220))

    def dibujar(self, seleccionado):
        color = (0, 0, 0)
        if seleccionado:
            color = (255, 0, 0)

        fuente = pygame.font.Font(None, 32)
        texto = fuente.render(self.texto, True, color)
        PANTALLA_JUEGO.blit(texto, (self.rect.x, self.rect.y))
        PANTALLA_JUEGO.blit(self.imagen, (self.rect.x, self.rect.y + 20))

    def esta_seleccionado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
