import pygame
import utils
import constantes

pygame.mixer.init()

def generar_musica(path: str, volumen: float):
    '''
    Función que se encarga de generar una música de fondo para mi juego
    Recibe el path donde se ubique mi música y el volumen de la misma
    '''
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volumen)

def generar_sonido(path: str, volumen: float):
    '''
    Función que se encarga de generar un sondi
    Recibe el path en donde se encuentra ese sonido y el volumen del mismo
    Retorna el sonido para esperar a que se ejecute
    '''
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(volumen)
    return sonido

def generar_texto(tamaño: float, contenido: str, color: tuple):
    '''
    Función que se encarga de generar un texto.
    Recibe la fuente, el tamaño de la misma, el contenido de ese texto y el color
    Retorna la superficie de ese texto
    '''
    fuente = pygame.font.SysFont("Arial Black", tamaño)
    return fuente.render(contenido, True, color)

def generar_imagen(fuente: str, tamaño: float, contenido: str, color: tuple):
    '''
    Función que se encarga de generar un texto.
    Recibe la fuente, el tamaño de la misma, el contenido de ese texto y el color
    Retorna la superficie de ese texto
    '''
    fuente = pygame.font.SysFont("Arial", tamaño)
    return fuente.render(contenido, True, color)


def mostrar_textos(pantalla_juego, cronometro=None, cantidad_movimientos=None):
    '''
    - Se encarga de fusionar los textos en la pantalla.
    - Recibe la pantalla del juego, el cronometro y la cantidad de movimientos.
    - No retorna nada
    '''
    texto_tiempo = utils.generar_texto(tamaño=25, contenido="seg", color=constantes.COLOR_NEGRO)
    pantalla_juego.blit(texto_tiempo, (constantes.ANCHO_PANTALLA /2 - 230, constantes.ALTO_PANTALLA - 35))
    
    texto_crono = utils.generar_texto(tamaño=50, contenido=str(cronometro), color=constantes.COLOR_NEGRO)
    pantalla_juego.blit(texto_crono, (constantes.ANCHO_PANTALLA /2 - 300, constantes.ALTO_PANTALLA - 60))
    
    texto_intentos = utils.generar_texto(tamaño=25, contenido="intentos", color=constantes.COLOR_NEGRO)
    pantalla_juego.blit(texto_intentos, (constantes.ANCHO_PANTALLA /2 + 190, constantes.ALTO_PANTALLA - 35))

    texto_movimientos = utils.generar_texto(tamaño=50, contenido=str(cantidad_movimientos // 2), color=constantes.COLOR_NEGRO)
    pantalla_juego.blit(texto_movimientos, (constantes.ANCHO_PANTALLA /2 + 120 , constantes.ALTO_PANTALLA - 60))  