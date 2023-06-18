import pygame
from pygame.locals import *
from personaje import Personaje, Vida
from enemigos import Enemigo
from constantes import *
from menu import Menu
from niveles import *

# Inicializar Pygame
pygame.init()
# Carga de imagenes
fondo_nivel_uno = pygame.image.load("Imagenes\\fondo-nivel-uno.jpg")
fondo_nivel_uno = pygame.transform.scale(fondo_nivel_uno, (ANCHO_PANTALLA, ALTO_PANTALLA))

imagen_nivel_uno = pygame.image.load("Imagenes\\previsualizacion-nivel-1.png")
imagen_nivel_uno = pygame.transform.scale(imagen_nivel_uno, (80, 80))

imagen_menu = pygame.image.load("Imagenes\\fondo-menu.jpg") 
imagen_menu = pygame.transform.scale(imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Crear el menú
opciones_menu = ["NIVEL I", "IN PROGRESS...", "IN PROGRESS..."]
menu = Menu(opciones_menu)
# Crear el personaje
personaje = Personaje()
# Creamos balas del personaje
grupo_balas = pygame.sprite.Group()
# Generamos el grupo de las vidas
vidas_personaje = pygame.sprite.Group()
for i in range(VIDAS_PERSONAJE):
    vida = Vida()
    vidas_personaje.add(vida)

# vidas_misil = pygame.sprite.Group()
# for i in range(2):
#     vida = Vida()
#     vidas_misil.add(vida)
# Crear un grupo para todos los misiles
grupo_misiles = pygame.sprite.Group()
# Crear misiles
for i in range(10):
    misil = Enemigo()
    grupo_misiles.add(misil)

# Textos
fuente = pygame.font.Font(None, 32)

font = pygame.font.SysFont("Arial Narrow", 50)
text = font.render("PERDISTE", True, (255, 0, 0))

# Variable de estado del juego
hubo_choque = False
# Bucle principal
reloj = pygame.time.Clock()
juego_corriendo = True
menu_activo = True
ingreso_nivel_uno = False
nivel_pausado = False


while juego_corriendo:
    # Manejar eventos de entrada
    for event in pygame.event.get():
        if event.type == QUIT:
            juego_corriendo = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if menu_activo:
                menu.actualizar_seleccion(mouse_pos)
                
                if menu.seleccion is not None and menu.seleccion.texto == "NIVEL I":
                    ingreso_nivel_uno = True
                    menu_activo = False
                #elif menu.seleccion is not None and menu.seleccion.texto == "Primer Nivel":
                    
    if menu_activo:
        PANTALLA_JUEGO.blit(imagen_menu, (0,0))
        menu.dibujar()
    else:
        if ingreso_nivel_uno:
            nivel_pausado = nivel_uno(personaje, grupo_misiles, hubo_choque, fondo_nivel_uno, grupo_balas, vidas_personaje)#, vidas_misil)
            if nivel_pausado:
                texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
                PANTALLA_JUEGO.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 80, ALTO_PANTALLA // 2 - 80))
                
    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)
    
# Salir del juego
pygame.quit()


