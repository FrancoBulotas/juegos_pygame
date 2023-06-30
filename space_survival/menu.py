import pygame
from constantes import *
from utilidades import *

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        #self.imagen_cerrar = pygame.image.load(RECURSOS + "menu\\iconos\\cruz-roja.png").convert_alpha()
        self.imagen_cerrar_juego = pygame.image.load(RECURSOS + "menu\\iconos\\cerrar.png").convert_alpha()
        self.imagen_cerrar_logros = pygame.image.load(RECURSOS + "menu\\iconos\\cruz_amarilla.png").convert_alpha()
        self.imagen_logros = pygame.image.load(RECURSOS + "menu\\iconos\\logros.png").convert_alpha()
        self.imagen_menu = pygame.image.load(RECURSOS + "menu\\fondo-menu.jpg").convert_alpha()
        self.imagen_menu = pygame.transform.scale(self.imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.imagen_cerrar_juego = pygame.transform.scale(self.imagen_cerrar_juego, (75, 75))
        self.imagen_cerrar_logros = pygame.transform.scale(self.imagen_cerrar_logros, (50, 50))
        self.imagen_logros = pygame.transform.scale(self.imagen_logros, (75, 75))
        self.rect_cerrar_juego = self.imagen_cerrar_juego.get_rect()
        self.rect_cerrar_juego.x = ANCHO_PANTALLA - 85
        self.rect_cerrar_juego.y = 10
        self.rect_cerrar_logros = self.imagen_cerrar_logros.get_rect()
        self.rect_cerrar_logros.center = ((ANCHO_PANTALLA // 2) + 210, ALTO_PANTALLA // 2 - 210)
        self.rect_logros = self.imagen_logros.get_rect()
        self.rect_logros.x = ANCHO_PANTALLA - 85
        self.rect_logros.y = 90
        
        self.imagen_fondo_logros =  pygame.image.load(RECURSOS + "menu\\menu-logros.png").convert_alpha()
        self.imagen_fondo_logros = pygame.transform.scale(self.imagen_fondo_logros, (600, 600))

        self.imagen_instrucciones = pygame.image.load(RECURSOS + "menu\\nube.png").convert_alpha()
        self.imagen_instrucciones = pygame.transform.scale(self.imagen_instrucciones, (450, 400))

        self.fuente_mejor_puntuacion = pygame.font.SysFont("Arial Black", 20)
        self.fuente_eliminaciones = pygame.font.SysFont("Arial Black", 20)


        for i, opcion in enumerate(opciones):
            x = 100 + (i * 350)
            y = ALTO_PANTALLA - 500 
            imagen = pygame.image.load(RECURSOS + "menu\\previsualizacion-nivel-{}.png".format(i + 1)).convert_alpha()
            self.opciones.append(Opcion(opcion, (x, y), imagen))

    def dibujar(self, cursor_nivel_uno, cursor_nivel_dos, cursor_nivel_tres):
        PANTALLA_JUEGO.blit(self.imagen_menu, (0,0))

        PANTALLA_JUEGO.blit(self.imagen_cerrar_juego, self.rect_cerrar_juego)
        PANTALLA_JUEGO.blit(self.imagen_logros, self.rect_logros)

        fuente_titulo = pygame.font.SysFont("Txt_IV25", 120)
        texto_titulo = fuente_titulo.render("Space Survival", True, (0,0,0))
        PANTALLA_JUEGO.blit(texto_titulo, (80,40))

        fuente_niveles = pygame.font.SysFont("Txt_IV25", 50)
        texto_niveles = fuente_niveles.render("Select Level", True,(0,0,0))
        PANTALLA_JUEGO.blit(texto_niveles, (120, ALTO_PANTALLA - 600 ))
        
        for opcion in self.opciones:
            opcion.dibujar()
  
        puntos_nivel_uno = traer_puntos_maximos_de_base(cursor_nivel_uno)
        if puntos_nivel_uno:
            self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_uno), True, (255,255,255))
            PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (160, ALTO_PANTALLA-190))

        puntos_nivel_dos = traer_puntos_maximos_de_base(cursor_nivel_dos)
        if puntos_nivel_dos:
            self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_dos), True, (255,255,255))
            PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (520, ALTO_PANTALLA-190))

        puntos_nivel_tres = traer_puntos_maximos_de_base(cursor_nivel_tres)
        if puntos_nivel_tres:
            self.texto_mejor_puntuacion = self.fuente_mejor_puntuacion.render("Best Score: " + str(puntos_nivel_tres), True, (255,255,255))
            PANTALLA_JUEGO.blit(self.texto_mejor_puntuacion, (870, ALTO_PANTALLA-190))

        PANTALLA_JUEGO.blit(self.imagen_instrucciones, (ANCHO_PANTALLA-400, ALTO_PANTALLA-400))


    def dibujar_menu_estadisticas(self, cursor_nivel_uno, cursor_nivel_dos, cursor_nivel_tres):
        PANTALLA_JUEGO.blit(self.imagen_fondo_logros, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 300))
        PANTALLA_JUEGO.blit(self.imagen_cerrar_logros, self.rect_cerrar_logros)
        # NIVEL 1
        eliminaciones_misiles_nivel_uno = suma_cantidad_eliminaciones(cursor_nivel_uno, misil=True)
        self.texto_eliminaciones = self.fuente_eliminaciones.render(str(eliminaciones_misiles_nivel_uno), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_eliminaciones, ((ANCHO_PANTALLA // 2) + 60,  ALTO_PANTALLA // 2 - 140))
        # NIVEL 2
        eliminaciones_aliens_nivel_dos = suma_cantidad_eliminaciones(cursor_nivel_dos, alien=True)
        self.texto_eliminaciones = self.fuente_eliminaciones.render(str(eliminaciones_aliens_nivel_dos), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_eliminaciones, ((ANCHO_PANTALLA // 2) + 60,  ALTO_PANTALLA // 2 - 8))
        eliminaciones_naves_nivel_dos = suma_cantidad_eliminaciones(cursor_nivel_dos, nave_alien=True)
        self.texto_eliminaciones = self.fuente_eliminaciones.render(str(eliminaciones_naves_nivel_dos), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_eliminaciones, ((ANCHO_PANTALLA // 2) + 60,  ALTO_PANTALLA // 2 + 19))
        # NIVEL 3
        eliminaciones_aliens_nivel_tres = suma_cantidad_eliminaciones(cursor_nivel_tres, alien=True)
        self.texto_eliminaciones = self.fuente_eliminaciones.render(str(eliminaciones_aliens_nivel_tres), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_eliminaciones, ((ANCHO_PANTALLA // 2) + 60,  ALTO_PANTALLA // 2 + 160))
        eliminaciones_naves_nivel_tres = suma_cantidad_eliminaciones(cursor_nivel_tres, nave_alien=True)
        self.texto_eliminaciones = self.fuente_eliminaciones.render(str(eliminaciones_naves_nivel_tres), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_eliminaciones, ((ANCHO_PANTALLA // 2) + 60,  ALTO_PANTALLA // 2 + 187))

    def actualizar_seleccion(self, mouse_pos):
        if self.rect_cerrar_juego.collidepoint(mouse_pos):
            self.seleccion = "salir"

        if self.rect_logros.collidepoint(mouse_pos):
            self.seleccion = "logros"
        if self.rect_cerrar_logros.collidepoint(mouse_pos):
            self.seleccion = "salir logros"

        for opcion in self.opciones:
            if opcion.esta_seleccionado(mouse_pos):
                self.seleccion = opcion.texto

    def sonido(self, sonidos, arrancar=False, parar=False, inicio_nivel=False):
        if arrancar:    
            sonidos.SONIDO_FONDO_MENU.play()
        if parar:
            sonidos.SONIDO_FONDO_MENU.stop()

        if inicio_nivel:
            sonidos.SONIDO_INICIAR_NIVEL.play()
    
        PANTALLA_JUEGO.blit(sonidos.texto_volumen, (ANCHO_PANTALLA-280, 15))


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
