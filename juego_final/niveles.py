import pygame
from constantes import *


class MenuNivel:
    def __init__(self, personaje) -> None:
        self.personaje = personaje

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png")
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
            
        self.imagen_fondo_menu =  pygame.image.load(RECURSOS + "menu\\menu-fin.png")
        self.imagen_fondo_menu = pygame.transform.scale(self.imagen_fondo_menu, (600, 600))

        
        self.imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\iconos\\repeat.png")
        self.rect_volver_a_jugar = self.imagen_volver_a_jugar.get_rect()
        self.rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 160
        self.rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 140  

        self.imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\iconos\\home.png")
        self.rect_volver_al_menu = self.imagen_volver_al_menu.get_rect()
        self.rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 230 
        self.rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 140   

        self.imagen_play = pygame.image.load(RECURSOS + "menu\\iconos\\play.png")
        self.rect_play = self.imagen_play.get_rect()
        self.rect_play.x = (ANCHO_PANTALLA // 2) - 30
        self.rect_play.y = ALTO_PANTALLA // 2 + 140

        self.imagen_ganador = pygame.image.load(RECURSOS + "menu\\WIN.png")
        self.imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png")

        # Parte negra superior
        self.imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png")
        self.imagen_superior = pygame.transform.scale(self.imagen_superior, (ANCHO_PANTALLA + 300, ALTURA_MENU_SUPERIOR))

        self.imagen_linea = pygame.image.load(RECURSOS + "fondo_niveles\\linea-recta.png")
        self.imagen_linea = pygame.transform.scale(self.imagen_linea, (ANCHO_PANTALLA, 40))
        # Contador disparos
        self.fuente = pygame.font.SysFont("Arial Black", 45)
        self.texto_municion = self.fuente.render(str(self.personaje.contador_municion), True, (255,255,255))

        self.imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png")


    def dibujar_barra_superior(self, cronometro) -> None:
        """
        - Se encarga de dibujar la barra superior del nivel.
        - No recibe nada.
        - No retorna nada.
        """
        self.cronometro = cronometro
        # Parte negra superior
        PANTALLA_JUEGO.blit(self.imagen_superior, (-150, -5))

        PANTALLA_JUEGO.blit(self.imagen_linea, (0, 60))
        # Contador disparos
        PANTALLA_JUEGO.blit(self.texto_municion, (50, 0))

        PANTALLA_JUEGO.blit(self.imagen_municion, (10,10))
        # Contador
        self.texto_crono = self.fuente.render(str(self.cronometro), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_crono, (ANCHO_PANTALLA/2, 0))

        self.rect_pausa.x = ANCHO_PANTALLA - 50
        self.rect_pausa.y = 10
        PANTALLA_JUEGO.blit(self.imagen_pausa, self.rect_pausa)


    def menu_fin(self, juego_en_pausa, nivel_terminado, resultado_ganador):
        """
        - Se encarga de dibujar el resultado del nivel, y de verificar si clickea volver a jugar o ir al menu.
        - Recibe la posicion del mouse.
        - Retorna si el menu esta activo(bool), si el nivel termino(bool) y la instacia del nivel uno creada nuevamente.
        """
        self.juego_en_pausa = juego_en_pausa
        self.nivel_terminado = nivel_terminado
        self.resultado_ganador = resultado_ganador
        PANTALLA_JUEGO.blit(self.imagen_fondo_menu, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 300))
                   
        PANTALLA_JUEGO.blit(self.imagen_volver_a_jugar, self.rect_volver_a_jugar)
                     
        PANTALLA_JUEGO.blit(self.imagen_volver_al_menu, self.rect_volver_al_menu)
        
        if self.juego_en_pausa and self.nivel_terminado:            
            PANTALLA_JUEGO.blit(self.imagen_play, self.rect_play)


        if self.resultado_ganador and not self.juego_en_pausa:
            PANTALLA_JUEGO.blit(self.imagen_ganador, ((ANCHO_PANTALLA // 2) - 170, ALTO_PANTALLA // 2 - 150))

        elif not self.resultado_ganador and not self.juego_en_pausa:
            PANTALLA_JUEGO.blit(self.imagen_perdedor, ((ANCHO_PANTALLA // 2) - 270, ALTO_PANTALLA // 2 - 150))


