import pygame
from constantes import *
import tablero
import utils

def terminar_partida(cronometro: int, cantidad_movimientos: int, tablero:dict):
    '''
    Verifico si el usuario ganó o perdio la partida
    si se queda sin movimientos o sin tiempo perdió 
    si todos las tarjetas del tablero están descubiertas el jugador gano
    Recibe el cronometro, los movimientos actuales del jugador y el tablero
    Si el jugador gano cambia la pantalla y muestra (VICTORIA O DERROTA DEPENDIENDO DE LO QUE HAYA PASADO)
    Retorna True si la partida termino y False si no lo terminó.
    '''
    if cronometro == 0:
        return True, 0
    elif cantidad_movimientos == 0:
        return True, 0
    else: 
        contador_acertadas = 0
        for tarjeta in tablero["tarjetas"]:
            if tarjeta["descubierto"] == True:
                contador_acertadas += 1
        
        if contador_acertadas == len(tablero["tarjetas"]):
            return True, contador_acertadas
        
    return False, 0

# Configuración inicial de pygame
pygame.init()
pantalla_juego = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Los Simpsons Memotest')
clock_fps = pygame.time.Clock() # Creamos un Clock para poder fijar los FPS

# Creamos eventos de tiempo
evento_1000ms = pygame.USEREVENT
pygame.time.set_timer(evento_1000ms, 1000)

# Configuracion inicial del juego
tablero_juego = tablero.crear_tablero()
cronometro = TIEMPO_JUEGO
cantidad_movimientos = CANTIDAD_INTENTOS
cantidad_tarjetas_cubiertas = CANTIDAD_TARJETAS_UNICAS * 2
cantidad_tarjetas_descubiertas = 0

# Textos
#texto_ganador = utils.generar_texto(tamaño=50, contenido="GANASTE", color=COLOR_NEGRO) #fuente_num.render("GANASTE", True, (0, 0, 0))
#texto_perdedor = utils.generar_texto(tamaño=50, contenido="PERDISTE", color=COLOR_BLANCO) #fuente_num.render("PERDISTE", True, (0, 0, 0))

texto_volver_a_jugar = utils.generar_texto(tamaño=30, contenido="VOLVER A JUGAR", color=COLOR_BLANCO)
rect_volver_a_jugar = texto_volver_a_jugar.get_rect()
rect_volver_a_jugar.centerx = ANCHO_PANTALLA / 2
rect_volver_a_jugar.centery = ALTO_PANTALLA / 2 + 180

# Imagenes
superficie_inicio = pygame.image.load(CARPETA_RECURSOS + "inicio.jpg")

imagen_fondo_ganador = pygame.image.load(CARPETA_RECURSOS + "Game_Over_Ganador.jpg")
imagen_fondo_ganador = pygame.transform.scale(imagen_fondo_ganador, (ANCHO_PANTALLA, ALTO_PANTALLA))

imagen_fondo_perdedor = pygame.image.load(CARPETA_RECURSOS + "Game_Over.jpg")
imagen_fondo_perdedor = pygame.transform.scale(imagen_fondo_perdedor, (ANCHO_PANTALLA, ALTO_PANTALLA))

imagen_start = pygame.image.load(CARPETA_RECURSOS + "start.png")
imagen_start = pygame.transform.scale(imagen_start, (200, 75))
rect_start = imagen_start.get_rect()

esta_corriendo = True
menu_activo = True
volvio_a_jugar = False
tiempo_parcial = 0
tiempo_en_menu = 0

while esta_corriendo:
    # Fijamos un valor de FPS
    clock_fps.tick(FPS)
    tiempo_actual_juego = pygame.time.get_ticks()
   
    # Manejamos los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esta_corriendo = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = event.pos
            SONIDO_CLICK.play()
            if tiempo_actual_juego - tiempo_en_menu > 200: # para que no se toque una carta al tocar start.
                if tablero.detectar_colision(tablero_juego, pos_mouse) != None and not menu_activo: 
                    SONIDO_VOLTEAR.play()
                    cantidad_movimientos -= 1

                if rect_volver_a_jugar.collidepoint(pos_mouse) and termino:
                    termino = False
                    cantidad_movimientos = CANTIDAD_INTENTOS
                    cronometro = TIEMPO_JUEGO

                    for tarjeta in tablero_juego["tarjetas"]:
                        tarjeta["visible"] = False
                        tarjeta["descubierto"] = False
                    
                    tablero_juego = tablero.crear_tablero()
                    tiempo_parcial = tiempo_actual_juego # esto esta para que una vez termine y quiera jugar de nuevo, se muestre el tiempo de previsualizacion.

            if rect_start.collidepoint(pos_mouse):
                menu_activo = False        

        # Cada vez que pase un segundo restamos uno al tiempo del cronometro
        if event.type == evento_1000ms and not termino and not menu_activo:
            cronometro -= 1

    # Verificamos si el juego termino
    termino, cantidad_acertadas = terminar_partida(cronometro, cantidad_movimientos, tablero_juego)
    if menu_activo:
        tablero.dibujar_menu(pantalla_juego, superficie_inicio, rect_start, imagen_start)     
        tiempo_en_menu = tiempo_actual_juego
    else:
        tiempo_actual_juego -= tiempo_en_menu
        if termino:
            pantalla_juego.fill(COLOR_BLANCO)
            if cronometro <= 0 or cantidad_movimientos == 0:
                pantalla_juego.blit(imagen_fondo_perdedor, (0,0))
                texto_volver_a_jugar = utils.generar_texto(tamaño=30, contenido="VOLVER A JUGAR", color=COLOR_BLANCO)

            elif cantidad_acertadas > 0:
                pantalla_juego.blit(imagen_fondo_ganador, (0,0))
                texto_volver_a_jugar = utils.generar_texto(tamaño=30, contenido="VOLVER A JUGAR", color=COLOR_NEGRO)
            
            pantalla_juego.blit(texto_volver_a_jugar, rect_volver_a_jugar)
            #pygame.display.flip()
        else:
            tablero.actualizar_tablero(tablero_juego)
            # Dibujar pantalla
            pantalla_juego.fill(COLOR_BLANCO) # Pintamos el fondo de color blanco
        
            tablero.dibujar_tablero(tablero_juego, pantalla_juego, (tiempo_actual_juego - tiempo_parcial))

            utils.mostrar_textos(pantalla_juego, cronometro, cantidad_movimientos)     
    # Mostramos los cambios hechos
    pygame.display.flip()

pygame.quit()
