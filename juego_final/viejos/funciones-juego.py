import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        #self.is_shooting = False
        self.missile_shot = False  # Variable de control para verificar si se disparó un misil

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.missile_shot:
            missile = Missile(self.rect.centerx, self.rect.top)
            missiles.add(missile)
            self.missile_shot = True
        elif not keys[pygame.K_SPACE]:
            self.missile_shot = False

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()  # Eliminar el misil cuando sale de la pantalla

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
missiles = pygame.sprite.Group()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    missiles.update()
    
    # Lógica de colisiones, dibujado de sprites, etc.
    
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    missiles.draw(screen)
    
    pygame.display.flip()

pygame.quit()