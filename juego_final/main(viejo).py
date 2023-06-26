import pygame
from pygame.locals import *
from personaje import Personaje, BalaExtra
from enemigos import Misil
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

# Generamos elementos/objetos nivel 1 
personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles = generar_elementos_nivel_uno()
# Textos
fuente = pygame.font.SysFont("Times New Roman", 32)
# Tiempo
tiempo_inicial = pygame.time.get_ticks()
tiempo_actual = 0
tiempo_previo = 0 
cronometro = TIEMPO_NIVEL
# Bucle principal
reloj = pygame.time.Clock()
juego_corriendo = True
menu_activo = True
ingreso_nivel_uno = False


nivel_terminado = False
resultado_ganador = False

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
                
                if menu.seleccion is not None and menu.seleccion == "salir":
                    juego_corriendo = False
                elif menu.seleccion is not None and menu.seleccion.texto == "NIVEL I":
                    ingreso_nivel_uno = True
                    menu_activo = False
                #elif menu.seleccion is not None and menu.seleccion.texto == "Primer Nivel":

    # Control del tiempo
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial  # Tiempo en milisegundos transcurridos desde el inicio del juego
    tiempo_actual = tiempo_transcurrido // 1000 # Tiempo en seg

    if tiempo_actual != tiempo_previo and ingreso_nivel_uno and not menu_activo:
        cronometro -= 1
    tiempo_previo = tiempo_actual

    if menu_activo:
        PANTALLA_JUEGO.blit(imagen_menu, (0,0))
        menu.dibujar()
    else:
        if ingreso_nivel_uno:
            # CREAR NIVEL UNO COMO OBJETO
            nivel_terminado, resultado_ganador = nivel_uno(personaje, grupo_misiles, fondo_nivel_uno, grupo_balas, vidas_personaje, cronometro, grupo_balas_extra, resultado_ganador)

            if nivel_terminado:
                resultado_ganador, menu_activo, nivel_terminado, cronometro, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles = menu_fin_nivel_uno(resultado_ganador, mouse_pos, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles)

    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)
    
# Salir del juego
pygame.quit()


