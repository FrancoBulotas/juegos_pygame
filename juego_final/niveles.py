import pygame
from constantes import *
from pygame.locals import *
import random

def nivel_uno(personaje, grupo_misiles, hubo_choque, fondo, grupo_balas, vidas_personaje, cronometro, grupo_balas_extra):
    teclas_presionadas = pygame.key.get_pressed()
    vida = personaje.vida

    # Obtener la posición del personaje y los objetos
    posicion_personaje = personaje.rect_nave
    # Verificar colisiones entre el personaje y los misiles
    for misil in grupo_misiles:
        posicion_misil = misil.rect
        if not misil.colision and posicion_personaje.colliderect(posicion_misil):
            hubo_choque = True
            misil.colision = True
            print("chocaste")
    # Verificar colisiones entre personaje y balas extra
    for bala_extra in grupo_balas_extra:
        if posicion_personaje.colliderect(bala_extra.rect):
            personaje.contador_municion += 5
            bala_extra.kill()
    # Si hubo un choque hace algo
    if hubo_choque:
        # Sacamos de a una vida si hubo un choque
        for vidas in vidas_personaje:
            vidas.kill()
            break
        personaje.vida -= 1
        hubo_choque = False

    PANTALLA_JUEGO.blit(fondo, (0, 70)) # Fondo de pantalla
    dibujar_parte_superior(personaje, cronometro)

    # Verificar el número de vidas del personaje
    if vida <= 0:
        return True

    # Actualizar la posición del personaje
    personaje.chequeo_teclas(teclas_presionadas, grupo_balas)
    # Agregamos municion extra
    # for i in range(3):    
    #     generar_municion_extra(i, lista_x_random, lista_y_random)
    grupo_balas_extra.update()

    # Actualizar y dibujar los misiles, balas y vidas
    for i in range(2):
        grupo_misiles.update(grupo_balas)

    grupo_balas.update()        

    for i in range(len(vidas_personaje)):
        vidas_personaje.update(personaje, i)

    grupo_misiles.draw(PANTALLA_JUEGO)
    grupo_balas.draw(PANTALLA_JUEGO)
    
    PANTALLA_JUEGO.blit(personaje.imagen_nave, personaje.rect_nave) # Dibuja la imagen del personaje

def dibujar_parte_superior(personaje, cronometro):
    # Parte negra superior
    imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png")
    imagen_superior = pygame.transform.scale(imagen_superior, (ANCHO_PANTALLA + 300, 80))
    PANTALLA_JUEGO.blit(imagen_superior, (-150, -5))

    imagen_linea = pygame.image.load(RECURSOS + "fondo_niveles\\linea-recta.png")
    imagen_linea = pygame.transform.scale(imagen_linea, (ANCHO_PANTALLA, 40))
    PANTALLA_JUEGO.blit(imagen_linea, (0, 60))
    # Contador disparos
    fuente = pygame.font.SysFont("Arial Black", 45)
    texto_municion = fuente.render(str(personaje.contador_municion), True, (255,255,255))
    PANTALLA_JUEGO.blit(texto_municion, (50, 0))
    imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png")
    PANTALLA_JUEGO.blit(imagen_municion, (10,10))
    # Contador
    texto_crono = fuente.render(str(cronometro), True, (255,255,255))
    PANTALLA_JUEGO.blit(texto_crono, (ANCHO_PANTALLA/2, 0))


def generar_municion_extra(i, lista_x_random, lista_y_random):
    imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png")
    rect_municion = imagen_municion.get_rect()
    rect_municion.x = lista_x_random[i]
    rect_municion.y = lista_y_random[i]
    PANTALLA_JUEGO.blit(imagen_municion, rect_municion)
