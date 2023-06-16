import pygame
from constantes import *


pygame.init()

fuente = pygame.font.Font(None, 32)



# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        for i, opcion in enumerate(opciones):
            x = ANCHO_PANTALLA // 2
            y = 200 + i * 60
            self.opciones.append(Opcion(opcion, (x, y)))

    def dibujar(self):
        for opcion in self.opciones:
            seleccionado = opcion is self.seleccion
            opcion.dibujar(seleccionado)

    def actualizar_seleccion(self, mouse_pos):
        for opcion in self.opciones:
            if opcion.esta_seleccionado(mouse_pos):
                self.seleccion = opcion
                break

    def ejecutar_accion(self):
        global juego_corriendo
        global ingreso_nivel_uno
        global menu_activo

        if self.seleccion is not None:
            opcion_seleccionada = self.seleccion.texto
            print("Seleccionaste:", opcion_seleccionada)

            if opcion_seleccionada == "Salir":
                juego_corriendo = False

            elif opcion_seleccionada == "Primer Nivel":
                ingreso_nivel_uno = True
                menu_activo = False

# Clase para representar una opción del menú
class Opcion:
    def __init__(self, texto, posicion):
        self.texto = texto
        self.posicion = posicion
        self.rect = pygame.Rect((0, 0), (200, 50))
        self.rect.center = posicion

    def dibujar(self, seleccionado):
        color = (0, 0, 0)
        if seleccionado:
            color = (255, 0, 0)
    
        texto = fuente.render(self.texto, True, color)

        screen.blit(texto, (self.rect.x, self.rect.y))
        
    def esta_seleccionado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
