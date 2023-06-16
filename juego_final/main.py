import pygame
from pygame.locals import *
from personaje import Personaje
from enemigos import Enemigos
from constantes import *
from menu import Menu


# Inicializar Pygame
pygame.init()

# Establecer el tamaño de la ventana
def chequeo_teclas(teclas_presionadas, imagen_nave):
    """
    - Verifica si se presiona alguna tecla, si se presiona, hace algo.
    - Recibe la tecla que se presiona.
    - Retorna la imagen de la nave, segun a donde esta apuntando.
    """
    if teclas_presionadas[K_a]:
        personaje.rect_nave.x -= VELOCIDAD
        
        imagen_nave = pygame.image.load("Imagenes\\nave-izquierda.png")
        return pygame.transform.scale(imagen_nave, (100, 50))
        
    if teclas_presionadas[K_d]:
        personaje.rect_nave.x += VELOCIDAD

        imagen_nave = pygame.image.load("Imagenes\\nave-derecha.png")
        return pygame.transform.scale(imagen_nave, (100, 50))
    
    if teclas_presionadas[K_w]:
        personaje.rect_nave.y -= VELOCIDAD

        imagen_nave = pygame.image.load("Imagenes\\nave-arriba.png")
        return pygame.transform.scale(imagen_nave, (50, 100))
    
    if teclas_presionadas[K_s]:
        personaje.rect_nave.y += VELOCIDAD

        imagen_nave = pygame.image.load("Imagenes\\nave-abajo.png")
        return pygame.transform.scale(imagen_nave, (50, 100))

    return imagen_nave


def primer_nivel(choque):

    teclas_presionadas = pygame.key.get_pressed()

    # Actualizar la posición del objeto
    imagen_nave = chequeo_teclas(teclas_presionadas, personaje.imagen_nave)

    # Dibujar el objeto en la ventana
    screen.blit(fondo, (0, 0)) # Fondo de pantalla

    # Obtener la posición del personaje y los objetos
    posicion_personaje = personaje.rect_nave
    # posiciones_misiles = [misil.rect for misil in grupo_objetos]

    # Verificar colisiones entre el personaje y los misiles
    for misil in grupo_objetos:
        posicion_misil = misil.rect
        if not misil.colision and posicion_personaje.colliderect(posicion_misil):
            choque = True
            misil.colision = True
            print("chocaste")

    # Si hubo un choque hace algo
    if choque:
        personaje.vida -= 1
        choque = False

    text_vida = font_vida.render("VIDA " + str(personaje.vida), True, (255, 0, 0))
    screen.blit(text_vida, (10, 10)) # Mensaje PERDISTE

    # Verificar el número de vidas del personaje
    if personaje.vida <= 0:
        return True
        
    # Actualizar y dibujar los objetos
    grupo_objetos.update()
    grupo_objetos.draw(screen)

    screen.blit(imagen_nave, personaje.rect_nave) # Dibuja la imagen del personaje


# Carga de imagenes
fondo = pygame.image.load("Imagenes\\fondo-nivel-uno.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

imagen_nivel_uno = pygame.image.load("Imagenes\\previsualizacion-nivel-1.png")
imagen_nivel_uno = pygame.transform.scale(imagen_nivel_uno, (80, 80))
#rect_nivel_uno = imagen_nivel_uno.get_rect()

imagen_menu = pygame.image.load("Imagenes\\fondo-menu.jpg") 
imagen_menu = pygame.transform.scale(imagen_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Crear el menú
opciones_menu = ["Juego Bulo", "Primer Nivel", "Salir"]
menu = Menu(opciones_menu)

# Crear el personaje
personaje = Personaje()

# Crear un grupo para todos los objetos
grupo_objetos = pygame.sprite.Group()

# Crear misiles
for _ in range(10):
    misil = Enemigos()
    grupo_objetos.add(misil)

# Textos
fuente = pygame.font.Font(None, 32)

font = pygame.font.SysFont("Arial Narrow", 50)
text = font.render("PERDISTE", True, (255, 0, 0))

font_vida = pygame.font.SysFont("Times New Roman", 20)
# Variable de estado del juego
choque = False

# Bucle principal
reloj = pygame.time.Clock()
juego_pausado = False
juego_corriendo = True
menu_activo = True
ingreso_nivel_uno = False

while juego_corriendo:
    # Manejar eventos de entrada
    for event in pygame.event.get():
        if event.type == QUIT:
            juego_corriendo = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if menu_activo:
                menu.actualizar_seleccion(mouse_pos)
                menu.ejecutar_accion()
                # if menu.seleccion is not None and menu.seleccion.texto == "Salir":
                #     juego_corriendo = False

                # elif menu.seleccion is not None and menu.seleccion.texto == "Primer Nivel":
                #     ingreso_nivel_uno = True
                #     menu_activo = False

    screen.fill((255, 255, 255))

    if menu_activo:
        screen.blit(imagen_menu, (0,0))
        menu.dibujar()
    else:
        if ingreso_nivel_uno:
            juego_pausado = primer_nivel(choque)
            if juego_pausado:
                #texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
                #screen.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 80, ALTO_PANTALLA // 2 - 80))
                pass

    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)

# Salir del juego
pygame.quit()


