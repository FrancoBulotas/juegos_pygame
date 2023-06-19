import pygame
from pygame.locals import *
from personaje import Personaje, Vida, BalaExtra
from enemigos import Enemigo
from constantes import *
from menu import Menu
from niveles import *

# Inicializar Pygame
pygame.init()
# Carga de imagenes
fondo_nivel_uno = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-uno3.png")
fondo_nivel_uno = pygame.transform.scale(fondo_nivel_uno, (ANCHO_PANTALLA, ALTO_PANTALLA))

imagen_nivel_uno = pygame.image.load(RECURSOS + "menu\\previsualizacion-nivel-1.png")
imagen_nivel_uno = pygame.transform.scale(imagen_nivel_uno, (80, 80))

imagen_menu = pygame.image.load(RECURSOS + "menu\\fondo-menu.jpg") 
imagen_menu = pygame.transform.scale(imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Crear el menú
opciones_menu = ["NIVEL I", "IN PROGRESS...", "IN PROGRESS..."]
menu = Menu(opciones_menu)
# Crear el personaje
personaje = Personaje()
# Creamos balas del personaje
grupo_balas = pygame.sprite.Group()

# Creamos balas extra
grupo_balas_extra = pygame.sprite.Group()
for i in range(3):
    bala = BalaExtra()
    grupo_balas_extra.add(bala)
# lista_x_random = [random.randint(20, ANCHO_PANTALLA-20), random.randint(20, ANCHO_PANTALLA-20), random.randint(20, ANCHO_PANTALLA-20)]
# lista_y_random = [random.randint(20, ALTO_PANTALLA-90), random.randint(20, ALTO_PANTALLA-90), random.randint(20, ALTO_PANTALLA-90)]

# for i in range(MUNICION_PERSONAJE)
#     bala = Bala
# Generamos el grupo de las vidas
vidas_personaje = pygame.sprite.Group()
for i in range(VIDAS_PERSONAJE):
    vida = Vida()
    vidas_personaje.add(vida)

# Crear un grupo para todos los misiles
grupo_misiles = pygame.sprite.Group()
# Crear misiles
for i in range(10):
    misil = Enemigo()
    grupo_misiles.add(misil)

# Textos
fuente = pygame.font.SysFont("Times New Roman", 32)
# Variable de estado del juego
hubo_choque = False
# Tiempo
tiempo_inicial = pygame.time.get_ticks()
tiempo_actual = 0
tiempo_previo = 0 
cronometro = 60
# Bucle principal
reloj = pygame.time.Clock()
juego_corriendo = True
menu_activo = True
ingreso_nivel_uno = False
nivel_pausado = False

while juego_corriendo:
    tiempo_actual_juego = pygame.time.get_ticks()
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

    # Control del tiempo
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial  # Tiempo en milisegundos transcurridos desde el inicio del juego
    tiempo_actual = tiempo_transcurrido // 1000 # Tiempo en seg

    if tiempo_actual != tiempo_previo and ingreso_nivel_uno:
        cronometro -= 1
    tiempo_previo = tiempo_actual

    if menu_activo:
        PANTALLA_JUEGO.blit(imagen_menu, (0,0))
        menu.dibujar()
    else:
        if ingreso_nivel_uno:
            nivel_pausado = nivel_uno(personaje, grupo_misiles, hubo_choque, fondo_nivel_uno, grupo_balas, vidas_personaje, cronometro, grupo_balas_extra)
            if nivel_pausado:
                texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
                PANTALLA_JUEGO.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 80, ALTO_PANTALLA // 2 - 80))
                
    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)
    
# Salir del juego
pygame.quit()


