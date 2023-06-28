import pygame
from constantes import *
from archivos import leer_archivo

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        self.imagen_cerrar = pygame.image.load(RECURSOS + "menu\\iconos\\cruz-roja.png").convert_alpha()
        self.imagen_menu = pygame.image.load(RECURSOS + "menu\\fondo-menu.jpg").convert_alpha()
        self.imagen_menu = pygame.transform.scale(self.imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.imagen_cerrar = pygame.transform.scale(self.imagen_cerrar, (50, 50))
        self.rect_cerrar = self.imagen_cerrar.get_rect()
        self.rect_cerrar.x = ANCHO_PANTALLA - 65
        self.rect_cerrar.y = 10

        self.fuente_mejor_puntuacion = pygame.font.SysFont("Arial Black", 20)

        for i, opcion in enumerate(opciones):
            x = 100 + (i * 350)
            y = ALTO_PANTALLA - 500 
            imagen = pygame.image.load(RECURSOS + "menu\\previsualizacion-nivel-{}.png".format(i + 1)).convert_alpha()
            self.opciones.append(Opcion(opcion, (x, y), imagen))

    def dibujar(self, archivo_puntos_lvl1, archivo_puntos_lvl2, archivo_puntos_lvl3):
        PANTALLA_JUEGO.blit(self.imagen_menu, (0,0))

        PANTALLA_JUEGO.blit(self.imagen_cerrar, self.rect_cerrar)

        fuente_titulo = pygame.font.SysFont("Txt_IV25", 120)
        texto_titulo = fuente_titulo.render("Space Survival", True, (0,0,0))
        PANTALLA_JUEGO.blit(texto_titulo, (80,40))

        fuente_niveles = pygame.font.SysFont("Txt_IV25", 50)
        texto_niveles = fuente_niveles.render("Select Level", True,(0,0,0))
        PANTALLA_JUEGO.blit(texto_niveles, (120, ALTO_PANTALLA - 600 ))
        
        for opcion in self.opciones:
            opcion.dibujar()
  
        puntos_nivel_uno = leer_archivo(archivo_puntos_lvl1)
        self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_uno), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (160, ALTO_PANTALLA-190))

        puntos_nivel_dos = leer_archivo(archivo_puntos_lvl2)
        self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_dos), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (520, ALTO_PANTALLA-190))

        puntos_nivel_tres = leer_archivo(archivo_puntos_lvl3)
        self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_tres), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (870, ALTO_PANTALLA-190))


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
