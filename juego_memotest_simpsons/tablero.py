import pygame
import time
import random
import tarjeta
from constantes import *


def crear_tablero():
    '''
    Crea una lista de tarjetas
    Retorna un dict tablero
    '''
    tablero = {}

    tablero["tarjetas"] = generar_lista_tarjetas()
    tablero["tiempo_ultimo_destape"] = 0
    tablero["primer_tarjeta_seleccionada"] = None
    tablero["segunda_tarjeta_seleccionada"] = None

    return tablero

def generar_lista_tarjetas()->list:
    '''
    Función que se encarga de generar una lista de tarjetas ordenada aleatoriamente
    El for x me recorre todas las posiciones de x usando de step el ancho de la tarjeta
    El for y me recorre todas las posiciones de x usando de step el alto de la tarjeta
    Por ende me va a generar la cantidad de tarjetas que le especifique anteriormente 
    ajustandose a la resolución de mi pantalla de manera dinámica
    Usa la función random.shuffle para generar de manera aleatoria los identificadores. Genera una lista de identificadores
    en donde se repiten dos veces el mismo ya que en un memotest se repiten dos veces la misma carta
    Retorna la lista de las tarjetas generadas
    '''
    lista_tarjetas = []
    indice = 0
    lista_id = generar_lista_ids_tarjetas() 
    #print(lista_id)

    for x in range(0, CANTIDAD_TARJETAS_H * ANCHO_TARJETA, ANCHO_TARJETA):
        for y in range(0, CANTIDAD_TARJETAS_V * ALTO_TARJETA, ALTO_TARJETA):
            identificador = lista_id[indice]
            nombre_imagen = "0" + str(lista_id[indice]) + ".png"
            nombre_imagen_escondida = "00.png"
            tarjeta_x = x
            tarjeta_y = y

            lista_tarjetas.append(tarjeta.crear_tarjeta(nombre_imagen, identificador, nombre_imagen_escondida, tarjeta_x, tarjeta_y))            
            
            indice += 1

    return lista_tarjetas

def generar_lista_ids_tarjetas():
    lista_id = list(range(1,CANTIDAD_TARJETAS_UNICAS+1)) #Creo una lista con todos los identificadores posibles
    lista_id.extend(list(range(1,CANTIDAD_TARJETAS_UNICAS+1))) #Extiendo esa lista con otra lista identica ya que hay dos tarjetas iguales en cada tablero (mismo identificador)
    random.seed(time.time())
    random.shuffle(lista_id) #Esos identificadores los desordeno de forma al azar
    return lista_id
    
def detectar_colision(tablero: dict, pos_xy: tuple) -> int  :
    '''
    verifica si existe una colision alguna tarjetas del tablero y la coordenada recibida como parametro
    Recibe como parametro el tablero y una tupla (X,Y)
    Retorna el identificador de la tarjeta que colisiono con el mouse y sino retorna None
    '''
    tiempo_actual = pygame.time.get_ticks()

    for tarjeta in tablero["tarjetas"]:
        # vemos si se cliquea, validamos que no se elijan mas de dos a la vez y que anteriormente no se haya clickeado.
        if tarjeta["rectangulo"].collidepoint(pos_xy) and tablero["segunda_tarjeta_seleccionada"] == None and not tarjeta["descubierto"]: 
            tarjeta["visible"] = True

            if tablero["primer_tarjeta_seleccionada"] == None:
                tablero["primer_tarjeta_seleccionada"] = tarjeta
            else:
                tablero["segunda_tarjeta_seleccionada"] = tarjeta

            tablero["tiempo_ultimo_destape"] = tiempo_actual

            return tarjeta["identificador"]


def actualizar_tablero(tablero: dict) -> None:
    '''
    Verifica si es necesario actualizar el estado de alguna tarjeta, en funcion de su propio estado y el de las otras
    Recibe como parametro el tablero
    '''
    tiempo_actual = pygame.time.get_ticks()

    if tiempo_actual - tablero["tiempo_ultimo_destape"] <= TIEMPO_MOVIMIENTO:                                                     
        if comprarar_tarjetas(tablero):
            tablero["primer_tarjeta_seleccionada"]["descubierto"] = True
            tablero["segunda_tarjeta_seleccionada"]["descubierto"] = True

            tablero["primer_tarjeta_seleccionada"]["visible"] = True
            tablero["segunda_tarjeta_seleccionada"]["visible"] = True

            tablero["primer_tarjeta_seleccionada"] = None
            tablero["segunda_tarjeta_seleccionada"] = None
        else:               
            if tiempo_actual - tablero["tiempo_ultimo_destape"] >= TIEMPO_MOVIMIENTO / 4: # para que no sea instantanio cuando se elije mal. 
                if tablero["primer_tarjeta_seleccionada"] and tablero["segunda_tarjeta_seleccionada"]:
                    tablero["primer_tarjeta_seleccionada"]["descubierto"] = False
                    tablero["segunda_tarjeta_seleccionada"]["descubierto"] = False

                    tablero["primer_tarjeta_seleccionada"]["visible"] = False
                    tablero["segunda_tarjeta_seleccionada"]["visible"] = False

                    tablero["primer_tarjeta_seleccionada"] = None
                    tablero["segunda_tarjeta_seleccionada"] = None
    else: # Si execede el tiempo de movimiento entra
        tablero["tiempo_ultimo_destape"] = 0
        
        for tarjeta in tablero["tarjetas"]:
            if tarjeta["descubierto"] == False:
                tarjeta["visible"] = False

        tablero["primer_tarjeta_seleccionada"] = None
        tablero["segunda_tarjeta_seleccionada"] = None


def comprarar_tarjetas(tablero: dict) -> bool | None:
    '''
    Funcion que se encarga de encontrar un match en la selección de las tarjetas del usuario.
    Si el usuario selecciono dos tarjetas está función se encargara de verificar si el identificador 
    de las mismas corresponde si es así retorna True, sino False. 
    En caso de que no hayan dos tarjetas seleccionadas retorna None
    '''
    retorno = None
    if tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None:
        retorno = False
        if tablero["primer_tarjeta_seleccionada"]["identificador"] == tablero["segunda_tarjeta_seleccionada"]["identificador"]:
            tarjeta.descubrir_tarjetas(tablero["tarjetas"], tablero["primer_tarjeta_seleccionada"]["identificador"])
            retorno = True

    return retorno

def dibujar_tablero(tablero: dict, pantalla_juego: pygame.Surface, tiempo_actual: int):
    '''
    Dibuja todos los elementos del tablero en la superficie recibida como parametro
    Recibe como parametro el tablero y la ventana principal
    '''
    for tarjeta in tablero["tarjetas"]:  
        if tiempo_actual <= TIEMPO_PREVISUALIZACION:
            pantalla_juego.blit(tarjeta["superficie"], tarjeta["rectangulo"])
        else:
            if tarjeta["visible"] == False:
                pantalla_juego.blit(tarjeta["superficie_escondida"], tarjeta["rectangulo"])
            else:
                pantalla_juego.blit(tarjeta["superficie"], tarjeta["rectangulo"])

        
def dibujar_menu(pantalla_juego, superficie_inicio, rect_start, imagen_start):
    """
    - Se encarga de mostrar en pantalla el menu.
    - Recibe la pantalla del juego.
    - No retorna nada.
    """
    superficie_inicio = pygame.transform.scale(superficie_inicio, (ANCHO_PANTALLA, ALTO_PANTALLA))
    rect_inicio = superficie_inicio.get_rect()

    pantalla_juego.blit(superficie_inicio, rect_inicio)

    rect_start.x = 205
    rect_start.y = 100
    pantalla_juego.blit(imagen_start, rect_start)