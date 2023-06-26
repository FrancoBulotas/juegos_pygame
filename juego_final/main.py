import pygame
from pygame.locals import *
from constantes import *
from menu import Menu
from nivel_uno import NivelUno
from nivel_dos import NivelDos
from nivel_tres import NivelTres

# Inicializar Pygame
pygame.init()
# Carga de imagenes
imagen_menu = pygame.image.load(RECURSOS + "menu\\fondo-menu.jpg") 
imagen_menu = pygame.transform.scale(imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Crear el menú
opciones_menu = ["NIVEL I", "NIVEL II", "NIVEL III"]
menu = Menu(opciones_menu)

# Generamos niveles
nivel_uno = NivelUno()
nivel_dos = NivelDos()
nivel_tres = NivelTres()
# Textos
fuente = pygame.font.SysFont("Times New Roman", 32)
# Tiempo
tiempo_inicial = pygame.time.get_ticks()
tiempo_actual = 0
tiempo_previo = 0 
# Bucle principal
reloj = pygame.time.Clock()
juego_corriendo = True
menu_activo = True


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
                # Para modificar la variable que se cambio al darle a volver a jugar
                nivel_uno.ingreso_nivel_uno = False
                nivel_dos.ingreso_nivel_dos = False

                if menu.seleccion is not None and menu.seleccion == "salir":
                    juego_corriendo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL I" and not nivel_uno.ingreso_nivel_uno:  
                    nivel_uno.ingreso_nivel_uno = True
                    nivel_tres.ingreso_nivel_tres = False
                    menu_activo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL II" and not nivel_dos.ingreso_nivel_dos:
                    nivel_dos.ingreso_nivel_dos = True   
                    nivel_tres.ingreso_nivel_tres = False 
                    menu_activo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL III" and not nivel_tres.ingreso_nivel_tres:
                    nivel_tres.ingreso_nivel_tres = True    
                    menu_activo = False

                menu.seleccion = ""

    # Control del tiempo
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial  # Tiempo en milisegundos transcurridos desde el inicio del juego
    tiempo_actual = tiempo_transcurrido // 1000 # Tiempo en seg

    if tiempo_actual != tiempo_previo and not menu_activo and nivel_uno.ingreso_nivel_uno and not nivel_uno.juego_en_pausa:
        nivel_uno.cronometro -= 1
        
    if tiempo_actual != tiempo_previo and not menu_activo and nivel_dos.ingreso_nivel_dos and not nivel_dos.juego_en_pausa:
        nivel_dos.cronometro -= 1

    if tiempo_actual != tiempo_previo and not menu_activo and nivel_tres.ingreso_nivel_tres and not nivel_tres.juego_en_pausa:
        nivel_tres.cronometro -= 1

    tiempo_previo = tiempo_actual

    if menu_activo:
        PANTALLA_JUEGO.blit(imagen_menu, (0,0))
        menu.dibujar()
    else:
        # NIVEL UNO
        if nivel_uno.ingreso_nivel_uno:
            nivel_uno.desarrollo(mouse_pos, nivel_uno)
            if nivel_uno.nivel_terminado:
                try:
                    menu_activo, nivel_uno = nivel_uno.menu_fin(mouse_pos)
                    # Esto es para que se pueda volver a jugar dandole a volver a jugar
                    nivel_uno.ingreso_nivel_uno = True
                except TypeError:
                    nivel_uno.nivel_terminado = True
                    menu_activo = False
        # NIVEL DOS 
        if nivel_dos.ingreso_nivel_dos:
            nivel_dos.desarrollo(mouse_pos, nivel_dos)
            if nivel_dos.nivel_terminado:
                try:
                    menu_activo, nivel_dos = nivel_dos.menu_fin(mouse_pos)
                    nivel_dos.ingreso_nivel_dos = True
                except TypeError:
                    nivel_dos.nivel_terminado = True
                    menu_activo = False
        # NIVEL TRES
        if nivel_tres.ingreso_nivel_tres:
            nivel_tres.desarrollo(mouse_pos, nivel_tres)
            if nivel_tres.nivel_terminado:
                try:
                    menu_activo, nivel_tres = nivel_tres.menu_fin(mouse_pos)
                    nivel_tres.ingreso_nivel_tres = True
                except TypeError:
                    nivel_tres.nivel_terminado = True
                    menu_activo = False

    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)
    
# Salir del juego
pygame.quit()


