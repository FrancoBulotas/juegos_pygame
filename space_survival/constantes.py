import pygame
import pyautogui

pygame.mixer.init()

def generar_sonido(ruta: str, volumen: float):
    '''
    Función que se encarga de generar un sondi
    Recibe la ruta en donde se encuentra ese sonido y el volumen del mismo
    Retorna el sonido para esperar a que se ejecute
    '''
    sonido = pygame.mixer.Sound(ruta)
    sonido.set_volume(volumen)
    return sonido

ANCHO_PANTALLA, ALTO_PANTALLA = pyautogui.size()

# ANCHO_PANTALLA = 1200
# ALTO_PANTALLA = 885

ANCHO_PERSONAJE = 100
ALTO_PERSONAJE = 50
ANCHO_MUNICION = 50
ALTO_MUNICION = 20

ALTURA_MENU_SUPERIOR = 80

VELOCIDAD_PERSONAJE = 8
VELOCIDAD_MISIL = 6
VELOCIDAD_NAVE_ALIEN = 4
VIDAS_PERSONAJE = 3
VIDA_MISIL = 2
VIDAS_NAVE_ALIEN_VIOLETA = 10
VIDAS_ALIEN = 1
MUNICION_PERSONAJE = 15
MUNICION_POR_BALAS_EXTRA = 5
MUNICION_POR_BALAS_EXTRA_MEJORADA = 3

TIEMPO_NIVEL = 60
CANTIDAD_MISILES_NIVEL_UN0 = 10
CANTIDAD_BALAS_EXTRA = 3
CANTIDAD_BALAS_EXTRA_MEJORADAS = 2
CANTIDAD_VIDAS_EXTRA = 1

PANTALLA_JUEGO = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
RECURSOS = "recursos\\"

# Puntuaciones
PUNTOS_POR_MISIL = 50
PUNTOS_POR_ALIEN = 25
PUNTOS_POR_NAVE_ALIEN = 300

# Sonidos
SONIDO_INICIAR_NIVEL = generar_sonido(RECURSOS + "sonidos\\menu\\start_button.wav", 1)  
SONIDO_HACIA_ATRAS = generar_sonido(RECURSOS + "sonidos\\menu\\back1.wav", 0.1)  
SONIDO_FONDO_MENU = generar_sonido(RECURSOS + "sonidos\\musica-fondo-menu.wav", 0.03) 
SONIDO_DISPARO_PERSONAJE = generar_sonido(RECURSOS + "sonidos\\switch_to_fire_bomb.wav", 0.08)
SONIDO_DISPARO_PERSONAJE_MEJORADO = generar_sonido(RECURSOS + "sonidos\\rocket_h3_3.wav", 0.08)
SONIDO_EXPLOSION_MISIL = generar_sonido(RECURSOS + "sonidos\\h3_small_expl4.wav", 0.08)
SONIDO_GOLPE_MISIL = generar_sonido(RECURSOS + "sonidos\\rocket_expl_lod_far1.wav", 0.08)
SONIDO_EXPLOSION_NAVE = generar_sonido(RECURSOS + "sonidos\\big_explosions3.wav", 0.03)





