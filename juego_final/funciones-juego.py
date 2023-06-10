import pygame
import random


# Inicializar pygame
pygame.init()

# Definir dimensiones de la pantalla
ancho_pantalla = 800
alto_pantalla = 600

# Crear la pantalla
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Movimiento del personaje")

# Definir colores
COLOR_FONDO = (255, 255, 255)
COLOR_PERSONAJE = (255, 0, 0)

# Clase para representar el personaje
class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(COLOR_PERSONAJE)
        self.rect = self.image.get_rect()
        self.rect.center = (ancho_pantalla // 2, alto_pantalla // 2)
        self.velocidad = 5  # Velocidad de movimiento del personaje

    def update(self):
        # Obtener el estado de las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Actualizar la posición del personaje según las teclas presionadas
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Mantener el personaje dentro de los límites de la pantalla
        self.rect.x = max(0, min(self.rect.x, ancho_pantalla - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, alto_pantalla - self.rect.height))

# Clase para representar los objetos
class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ancho_pantalla - self.rect.width)
        self.rect.y = random.randint(0, alto_pantalla - self.rect.height)

# Crear el personaje
personaje = Personaje()

# Crear un grupo para todos los objetos
grupo_objetos = pygame.sprite.Group()

# Crear objetos
for _ in range(10):
    objeto = Objeto()
    grupo_objetos.add(objeto)

# Bucle principal del juego
juego_en_ejecucion = True
reloj = pygame.time.Clock()

while juego_en_ejecucion:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_en_ejecucion = False

    pantalla.fill(COLOR_FONDO)

    # Obtener la posición del personaje y los objetos
    posicion_personaje = personaje.rect
    posiciones_objetos = [objeto.rect for objeto in grupo_objetos]

    for posicion_objeto in posiciones_objetos:
        if posicion_personaje.colliderect(posicion_objeto):
            # Realizar la acción que deseas cuando ocurre una colisión
            print("¡Colisión detectada!")


    grupo_objetos.update()
    grupo_objetos.draw(pantalla)
    # Actualizar y dibujar el personaje
    personaje.update()
    pantalla.blit(personaje.image, personaje.rect)

    pygame.display.flip()
    reloj.tick(60)

# Salir del programa
pygame.quit()