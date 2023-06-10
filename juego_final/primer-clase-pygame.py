import pygame
from pygame.locals import *
import random

# Inicializar Pygame
pygame.init()

# Establecer el tamaño de la ventana
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

# Establecer la velocidad de movimiento
velocidad = 7

def chequeo_teclas(teclas_presionadas, imagen_nave):
    """
    - Verifica si se presiona alguna tecla, si se presiona, hace algo.
    - Recibe la tecla que se presiona.
    - Retorna la imagen de la nave, segun a donde esta apuntando.
    """
    if teclas_presionadas[K_a]:
        personaje.rect_nave.x -= velocidad
        
        imagen_nave = pygame.image.load("Imagenes\\nave-izquierda.png")
        return pygame.transform.scale(imagen_nave, (100, 50))
        
    if teclas_presionadas[K_d]:
        personaje.rect_nave.x += velocidad

        imagen_nave = pygame.image.load("Imagenes\\nave-derecha.png")
        return pygame.transform.scale(imagen_nave, (100, 50))
    
    if teclas_presionadas[K_w]:
        personaje.rect_nave.y -= velocidad

        imagen_nave = pygame.image.load("Imagenes\\nave-arriba.png")
        return pygame.transform.scale(imagen_nave, (50, 100))
    
    if teclas_presionadas[K_s]:
        personaje.rect_nave.y += velocidad

        imagen_nave = pygame.image.load("Imagenes\\nave-abajo.png")
        return pygame.transform.scale(imagen_nave, (50, 100))

    return imagen_nave


def primer_nivel(juego_pausado_1, choque_1):

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
            choque_1 = True
            misil.colision = True
            print("chocaste")

    # Si hubo un choque hace algo
    if choque_1:
        personaje.vida -= 1
        choque_1 = False

    text_vida = font_vida.render("VIDA " + str(personaje.vida), True, (255, 0, 0))
    screen.blit(text_vida, (10, 10)) # Mensaje PERDISTE

    # Verificar el número de vidas del personaje
    if personaje.vida <= 0:
        juego_pausado_1 = True
        return juego_pausado_1

    # Actualizar y dibujar los objetos
    grupo_objetos.update()
    grupo_objetos.draw(screen)

    screen.blit(imagen_nave, personaje.rect_nave) # Dibuja la imagen del personaje


fuente = pygame.font.Font(None, 32)

# Clase para representar una opción del menú
class Opcion:
    def __init__(self, texto, posicion):
        self.texto = texto
        self.posicion = posicion
        self.rect = pygame.Rect((0, 0), (200, 50))
        self.rect.center = posicion

    def dibujar(self, seleccionado):
        color = (0, 0, 0)
        if seleccionado:
            color = (255, 0, 0)
        texto = fuente.render(self.texto, True, color)
        screen.blit(texto, (self.rect.x, self.rect.y))

    def esta_seleccionado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Clase para representar el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        self.seleccion = None
        for i, opcion in enumerate(opciones):
            x = width // 2
            y = 200 + i * 60
            self.opciones.append(Opcion(opcion, (x, y)))

    def dibujar(self):
        for opcion in self.opciones:
            seleccionado = opcion is self.seleccion
            opcion.dibujar(seleccionado)

    def actualizar_seleccion(self, mouse_pos):
        for opcion in self.opciones:
            if opcion.esta_seleccionado(mouse_pos):
                self.seleccion = opcion
                break

    def ejecutar_accion(self):
        if self.seleccion is not None:
            opcion_seleccionada = self.seleccion.texto
            print("Seleccionaste:", opcion_seleccionada)
            # Aquí puedes agregar la lógica correspondiente a cada opción del menú

# Crear el menú
opciones_menu = ["Iniciar juego", "Salir"]
menu = Menu(opciones_menu)

# Clase para representar el personaje
class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_nave = pygame.image.load("Imagenes\\nave-arriba.png")
        self.imagen_nave = pygame.transform.scale(self.imagen_nave, (50, 100))
        self.rect_nave = self.imagen_nave.get_rect()
        self.vida = 3

# Clase para representar los misiles
class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes\\cohete-arriba.png")
        self.image = pygame.transform.scale(self.image, (40, 80))
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.velocidad_x = random.randint(-7, 7)
        self.velocidad_y = random.randint(-7, 7)
        self.colision = False

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left < 0:
            self.velocidad_x *= -1
            self.image = pygame.image.load("Imagenes\\cohete-derecha.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.right > width:
            self.velocidad_x *= -1
            self.image = pygame.image.load("Imagenes\\cohete-izquierda.png")
            self.image = pygame.transform.scale(self.image, (80, 40))

        if self.rect.top < 0:
            self.velocidad_y *= -1
            self.image = pygame.image.load("Imagenes\\cohete-abajo.png")
            self.image = pygame.transform.scale(self.image, (40, 80))

        if self.rect.bottom > height:
            self.velocidad_y *= -1
            self.image = pygame.image.load("Imagenes\\cohete-arriba.png")
            self.image = pygame.transform.scale(self.image, (40, 80))

# Carga de imagenes
fondo = pygame.image.load("Imagenes\\fondo.jpg")
fondo = pygame.transform.scale(fondo, (width, height))

# Crear el personaje
personaje = Personaje()

# Crear un grupo para todos los objetos
grupo_objetos = pygame.sprite.Group()

# Crear objetos
for _ in range(10):
    objeto = Objeto()
    grupo_objetos.add(objeto)

# Textos
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
                if menu.seleccion is not None and menu.seleccion.texto == "Salir":
                    juego_corriendo = False

                elif menu.seleccion is not None and menu.seleccion.texto == "Iniciar juego":
                    ingreso_nivel_uno = True
                    menu_activo = False

    screen.fill((255, 255, 255))

    if menu_activo:
        menu.dibujar()
    else:
        if ingreso_nivel_uno:
            juego_pausado = primer_nivel(juego_pausado, choque)
            if juego_pausado:
                texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
                screen.blit(texto_game_over, (width // 2 - 80, height // 2 - 80))

    pygame.display.flip() # Actualizar la pantalla
    reloj.tick(60)

# Salir del juego
pygame.quit()


