import pygame
from constantes import *
from pygame.locals import *


def nivel_uno(personaje, grupo_misiles, hubo_choque, fondo, grupo_balas, vidas_personaje):#, vidas_misil):
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
    
    # Si hubo un choque hace algo
    if hubo_choque:
        # Sacamos de a una vida si hubo un choque
        for vidas in vidas_personaje:
            vidas.kill()
            break
        personaje.vida -= 1
        hubo_choque = False

    PANTALLA_JUEGO.blit(fondo, (0, 0)) # Fondo de pantalla
    # Verificar el número de vidas del personaje
    if vida <= 0:
        return True

    # Actualizar la posición del personaje
    personaje.chequeo_teclas(teclas_presionadas, grupo_balas)
    # Actualizar y dibujar los misiles, balas y vidas
    for i in range(2):
        grupo_misiles.update(grupo_balas)

    grupo_balas.update()        

    for i in range(len(vidas_personaje)):
        vidas_personaje.update(personaje, i)

    grupo_misiles.draw(PANTALLA_JUEGO)
    grupo_balas.draw(PANTALLA_JUEGO)
    
    PANTALLA_JUEGO.blit(personaje.imagen_nave, personaje.rect_nave) # Dibuja la imagen del personaje
        