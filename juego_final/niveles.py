import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra
from vida import Vida
from enemigos import Enemigo

def generar_elementos_nivel_uno():
    # Crear el personaje
    personaje = Personaje()
    # Creamos balas del personaje
    grupo_balas = pygame.sprite.Group()
    # Creamos balas extra
    grupo_balas_extra = pygame.sprite.Group()
    for i in range(CANTIDAD_BALAS_EXTRA_NIVEL_UNO):
        bala = BalaExtra()
        grupo_balas_extra.add(bala)

    # Generamos el grupo de las vidas
    vidas_personaje = pygame.sprite.Group()
    for i in range(VIDAS_PERSONAJE):
        vida = Vida()
        vidas_personaje.add(vida)

    # Crear un grupo para todos los misiles
    grupo_misiles = pygame.sprite.Group()
    # Crear misiles
    for i in range(CANTIDAD_MISILES_NIVEL_UN0):
        misil = Enemigo()
        grupo_misiles.add(misil)
    
    return personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles


def menu_fin_nivel_uno(resultado_ganador, mouse_pos, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles):
    imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\repeat.png")
    rect_volver_a_jugar = imagen_volver_a_jugar.get_rect()
    rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 170
    rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 80                        
    PANTALLA_JUEGO.blit(imagen_volver_a_jugar, rect_volver_a_jugar)

    imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\home.png")
    rect_volver_al_menu = imagen_volver_al_menu.get_rect()
    rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 300 
    rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 80                        
    PANTALLA_JUEGO.blit(imagen_volver_al_menu, rect_volver_al_menu)
    
    if pygame.mouse.get_pressed()[0]:
        if rect_volver_a_jugar.collidepoint(mouse_pos):
            personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles = generar_elementos_nivel_uno()
            return None, False, False, TIEMPO_NIVEL_UNO, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles
        
        if rect_volver_al_menu.collidepoint(mouse_pos):
            personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles = generar_elementos_nivel_uno()
            return None, True, False, TIEMPO_NIVEL_UNO, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles

    if resultado_ganador:
        imagen_ganador = pygame.image.load(RECURSOS + "menu\\WINNER.png")
        PANTALLA_JUEGO.blit(imagen_ganador, ((ANCHO_PANTALLA // 2) - 350, ALTO_PANTALLA // 2 - 80))
    else:
        imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png")
        PANTALLA_JUEGO.blit(imagen_perdedor, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 80))
  
    return resultado_ganador, False, True, -1, personaje, grupo_balas, grupo_balas_extra, vidas_personaje, grupo_misiles    


def nivel_uno(personaje, grupo_misiles, fondo, grupo_balas, vidas_personaje, cronometro, grupo_balas_extra, resultado_ganador):
    teclas_presionadas = pygame.key.get_pressed()
    vida_personaje = personaje.vida

    # Verificar colisiones
    verificar_colisiones(personaje, grupo_misiles, vidas_personaje, grupo_balas_extra)
    
    # Chequear variables del estado del juego
    fin_nivel, cronometro, resultado_ganador = chequeo_estado_juego(vida_personaje, cronometro, grupo_misiles, resultado_ganador)
    if fin_nivel:
        return fin_nivel, resultado_ganador

    PANTALLA_JUEGO.blit(fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
    dibujar_parte_superior(personaje, cronometro)    
    # Actualizar la posición del personaje
    personaje.chequeo_teclas(teclas_presionadas, grupo_balas)
    # Agregamos municion extra
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
        # fin_nivel, resultado_ganador
    return False, resultado_ganador


def dibujar_parte_superior(personaje, cronometro):
    # Parte negra superior
    imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png")
    imagen_superior = pygame.transform.scale(imagen_superior, (ANCHO_PANTALLA + 300, ALTURA_MENU_SUPERIOR))
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


def verificar_colisiones(personaje, grupo_misiles, vidas_personaje, grupo_balas_extra):
    # Obtener la posición del personaje y los objetos
    posicion_personaje = personaje.rect_nave

    # Verificar colisiones entre el personaje y los misiles
    for misil in grupo_misiles:
        posicion_misil = misil.rect
        # Si misil.colision es False, y el misil esta chocando con el personaje entra.
        if not misil.colision and posicion_personaje.colliderect(posicion_misil):
            # Sacamos de a una vida si hubo un choque
            for vidas in vidas_personaje:
                vidas.kill()
                break
            personaje.vida -= 1

            misil.colision = True
        # Si el misil no le esta pegando al personaje, misil.colision vuelve a false.
        if not posicion_personaje.colliderect(posicion_misil): 
            misil.colision = False

    # Verificar colisiones entre personaje y balas extra
    for bala_extra in grupo_balas_extra:
        if posicion_personaje.colliderect(bala_extra.rect):
            personaje.contador_municion += 5
            bala_extra.kill()

def chequeo_estado_juego(vida_personaje, cronometro, grupo_misiles, resultado_ganador):
    # Verificar el número de vidas del personaje
    if vida_personaje <= 0:
            # fin_nivel, cronometro, resultado_ganador 
        return True, 0, False
    elif len(grupo_misiles) <= 0:
        return True, 0, True
    elif cronometro < 0:
        return True, 0, False

    return False, cronometro, resultado_ganador