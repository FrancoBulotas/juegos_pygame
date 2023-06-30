import pygame
from pygame.locals import *
from constantes import *
from menu import Menu
from nivel_uno import NivelUno
from nivel_dos import NivelDos
from nivel_tres import NivelTres
from utilidades import *
import sqlite3


# Inicializar Pygame
pygame.init()
# Crear el menú
opciones_menu = ["NIVEL I", "NIVEL II", "NIVEL III"]
menu = Menu(opciones_menu)
# Audio
volumen = leer_archivo_volumen()
sonidos = Sonidos(volumen)
# Generamos niveles
nivel_uno = NivelUno()
nivel_dos = NivelDos()
nivel_tres = NivelTres()
# Textos
#entrada_texto = pygame.input.TextInput()
# Tiempo
tiempo_inicial = pygame.time.get_ticks()
tiempo_actual = 0
tiempo_previo = 0 
# Bucle principal
reloj = pygame.time.Clock()
juego_corriendo = True
menu_activo = True

# Archivos / Base de datos
# flag_archivo_guardado = False
# nivel_uno.archivo_puntos = obtener_nombre_archivo_puntos(nivel_uno=True)
# nivel_dos.archivo_puntos = obtener_nombre_archivo_puntos(nivel_dos=True)
# nivel_tres.archivo_puntos = obtener_nombre_archivo_puntos(nivel_tres=True)
conexion_nivel_uno, cursor_nivel_uno = crear_base_y_cursor(nivel=1)
conexion_nivel_dos, cursor_nivel_dos = crear_base_y_cursor(nivel=2)
conexion_nivel_tres, cursor_nivel_tres = crear_base_y_cursor(nivel=3)

while juego_corriendo:
    tiempo_actual_juego = pygame.time.get_ticks()
    # Manejar eventos de entrada
    for evento in pygame.event.get():
        if evento.type == QUIT:
            juego_corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if menu_activo:
                menu.actualizar_seleccion(mouse_pos)
                # Para modificar la variable que se cambio al darle a volver a jugar
                nivel_uno.ingreso_nivel = False
                nivel_dos.ingreso_nivel = False
                nivel_tres.ingreso_nivel = False 

                if menu.seleccion is not None and menu.seleccion == "salir":
                    guardar_archivo_volumen(sonidos.volumen)
                    juego_corriendo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL I" and not nivel_uno.ingreso_nivel: 
                    nivel_uno.ingreso_nivel = True
                    menu_activo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL II" and not nivel_dos.ingreso_nivel:
                    nivel_dos.ingreso_nivel = True    
                    menu_activo = False
                elif menu.seleccion is not None and menu.seleccion == "NIVEL III" and not nivel_tres.ingreso_nivel:
                    nivel_tres.ingreso_nivel = True    
                    menu_activo = False
                menu.seleccion = ""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                #volumen = regular_volumen(volumen, sube=True)  
                sonidos.regular_volumen(sube=True)
            elif evento.key == pygame.K_DOWN:
                #volumen = regular_volumen(volumen, baja=True)
                sonidos.regular_volumen(baja=True)
                
    # Control del tiempo
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial  # Tiempo en milisegundos transcurridos desde el inicio del juego
    tiempo_actual = tiempo_transcurrido // 1000 # Tiempo en seg

    if tiempo_actual != tiempo_previo and not menu_activo and nivel_uno.ingreso_nivel and not nivel_uno.juego_en_pausa:
        nivel_uno.cronometro -= 1     
    if tiempo_actual != tiempo_previo and not menu_activo and nivel_dos.ingreso_nivel and not nivel_dos.juego_en_pausa:
        nivel_dos.cronometro -= 1
    if tiempo_actual != tiempo_previo and not menu_activo and nivel_tres.ingreso_nivel and not nivel_tres.juego_en_pausa:
        nivel_tres.cronometro -= 1

    tiempo_previo = tiempo_actual

    if menu_activo:
        menu.dibujar(cursor_nivel_uno, cursor_nivel_dos, cursor_nivel_tres) 
        menu.sonido(sonidos, arrancar=True)
    else:
        menu.sonido(sonidos, parar=True)
        # NIVEL UNO
        if nivel_uno.ingreso_nivel:
            nivel_uno.desarrollo(mouse_pos, nivel_uno, sonidos, cursor_nivel_uno, conexion_nivel_uno)
            menu_activo = nivel_uno.menu_activo
            nivel_uno = nivel_uno.nivel
        # NIVEL DOS 
        if nivel_dos.ingreso_nivel:
            nivel_dos.desarrollo(mouse_pos, nivel_dos, sonidos, cursor_nivel_dos, conexion_nivel_dos)
            menu_activo = nivel_dos.menu_activo
            nivel_dos = nivel_dos.nivel
        # NIVEL TRES
        if nivel_tres.ingreso_nivel:
            nivel_tres.desarrollo(mouse_pos, nivel_tres, sonidos, cursor_nivel_tres, conexion_nivel_tres)
            menu_activo = nivel_tres.menu_activo
            nivel_tres = nivel_tres.nivel

    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)


conexion_nivel_uno.close()
conexion_nivel_dos.close()
conexion_nivel_tres.close()
# Salir del juego
pygame.quit()


