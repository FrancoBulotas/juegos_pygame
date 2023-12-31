import pygame
from constantes import *
import random


class GeneralNiveles:
    def __init__(self, personaje, sonidos) -> None:
        self.personaje = personaje

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png").convert_alpha()
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
            
        self.imagen_fondo_menu =  pygame.image.load(RECURSOS + "menu\\menu-fin.png").convert_alpha()
        self.imagen_fondo_menu = pygame.transform.scale(self.imagen_fondo_menu, (600, 600))

        
        self.imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\iconos\\repeat.png").convert_alpha()
        self.rect_volver_a_jugar = self.imagen_volver_a_jugar.get_rect()
        self.rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 160
        self.rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 140  

        self.imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\iconos\\home.png").convert_alpha()
        self.rect_volver_al_menu = self.imagen_volver_al_menu.get_rect()
        self.rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 230 
        self.rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 140   

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png").convert_alpha()
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
        self.rect_pausa.x = ANCHO_PANTALLA - 50
        self.rect_pausa.y = 10
    
        self.imagen_play = pygame.image.load(RECURSOS + "menu\\iconos\\play.png").convert_alpha()
        self.rect_play = self.imagen_play.get_rect()
        self.rect_play.x = (ANCHO_PANTALLA // 2) - 30
        self.rect_play.y = ALTO_PANTALLA // 2 + 140
        # Menu pausado
        self.imagen_paused = pygame.image.load(RECURSOS + "menu\\paused.png").convert_alpha()
        self.imagen_ganador = pygame.image.load(RECURSOS + "menu\\WIN.png").convert_alpha()
        self.imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png").convert_alpha()

        # Parte negra superior
        self.imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png").convert_alpha()
        self.imagen_superior = pygame.transform.scale(self.imagen_superior, (ANCHO_PANTALLA + 300, ALTURA_MENU_SUPERIOR))

        self.imagen_linea = pygame.image.load(RECURSOS + "fondo_niveles\\linea-recta.png").convert_alpha()
        self.imagen_linea = pygame.transform.scale(self.imagen_linea, (ANCHO_PANTALLA, 40))
        # Contador disparos
        self.fuente = pygame.font.SysFont("Arial Black", 45)
        self.texto_puntos = self.fuente.render("Total Points ", True, (255,255,255))
        self.imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png").convert_alpha()

        self.imagen_municion_mejorada = pygame.image.load(RECURSOS + "personaje\\municion-mejorada-extra.png").convert_alpha()
        self.imagen_municion_mejorada = pygame.transform.scale(self.imagen_municion_mejorada, (50,50))

        self.sonidos = sonidos
        self.fondo_estrellas = pygame.Surface((ANCHO_FONDO_ESTRELLAS, ALTO_FONDO_ESTRELLAS), pygame.SRCALPHA)
        self.fondo_estrellas.fill((0, 0, 0, 0))

    def dibujar_barra_superior(self, nivel, nivel_tres=False) -> None:
        """
        - Se encarga de dibujar la barra superior del nivel.
        - No recibe nada.
        - No retorna nada.
        """
        #self.cronometro = cronometro
        #self.sonidos.SONIDO_FONDO_NIVEL.play()

        # Parte negra superior
        PANTALLA_JUEGO.blit(self.imagen_superior, (-150, -5))

        PANTALLA_JUEGO.blit(self.imagen_linea, (0, 60))
        # Contador disparos
        self.texto_municion = self.fuente.render(str(nivel.personaje.contador_municion), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_municion, (50, 0))
        PANTALLA_JUEGO.blit(self.imagen_municion, (10,10))
        if nivel_tres:
            self.texto_municion_mejorada = self.fuente.render(str(nivel.personaje.contador_municion_mejorada), True, (255,255,255))
            PANTALLA_JUEGO.blit(self.texto_municion_mejorada, (210, 0))
            PANTALLA_JUEGO.blit(self.imagen_municion_mejorada, (150,8))
        # Contador
        self.texto_crono = self.fuente.render(str(nivel.cronometro), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_crono, (ANCHO_PANTALLA/2, 0))
        # Contador puntos
        self.texto_cant_puntos = self.fuente.render(str(nivel.contador_puntos), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_cant_puntos, (ANCHO_PANTALLA/2 - 400, 0))

        PANTALLA_JUEGO.blit(self.imagen_pausa, self.rect_pausa)


    def dibujar_menu_fin(self, nivel, sonidos):
        """
        - Se encarga de dibujar el resultado del nivel, y de verificar si clickea volver a jugar o ir al menu.
        - Recibe la instancia del nivel.
        - No retorna nada.
        """
        PANTALLA_JUEGO.blit(self.imagen_fondo_menu, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 300))
                   
        PANTALLA_JUEGO.blit(self.imagen_volver_a_jugar, self.rect_volver_a_jugar)
                     
        PANTALLA_JUEGO.blit(self.imagen_volver_al_menu, self.rect_volver_al_menu)
        
        if nivel.juego_en_pausa and nivel.nivel_terminado:    
            PANTALLA_JUEGO.blit(self.imagen_paused, ((ANCHO_PANTALLA // 2) - 125, ALTO_PANTALLA // 2 - 150))        
            PANTALLA_JUEGO.blit(self.imagen_play, self.rect_play)
            PANTALLA_JUEGO.blit(sonidos.texto_volumen, ((ANCHO_PANTALLA // 2) - 90, ALTO_PANTALLA // 2 - 20))

        if nivel.resultado_ganador and not nivel.juego_en_pausa:
            PANTALLA_JUEGO.blit(self.imagen_ganador, ((ANCHO_PANTALLA // 2) - 170, ALTO_PANTALLA // 2 - 150))

        elif not nivel.resultado_ganador and not nivel.juego_en_pausa:
            PANTALLA_JUEGO.blit(self.imagen_perdedor, ((ANCHO_PANTALLA // 2) - 270, ALTO_PANTALLA // 2 - 150))

        PANTALLA_JUEGO.blit(self.texto_puntos, ((ANCHO_PANTALLA // 2) - 210, ALTO_PANTALLA // 2 + 10))
        PANTALLA_JUEGO.blit(self.texto_cant_puntos, ((ANCHO_PANTALLA // 2) + 150, ALTO_PANTALLA // 2 + 10))

        pygame.draw.rect(PANTALLA_JUEGO, (0,0,0), (ANCHO_PANTALLA-280, 12, 140, 40))

    
    def eleccion_menu_fin(self, mouse_pos, nivel):
        if pygame.mouse.get_pressed()[0] and nivel.nivel_terminado:
            if self.rect_volver_a_jugar.collidepoint(mouse_pos):
                self.sonido(hacia_atras=True)
                nivel.nivel = nivel.generar_instancia_nivel()                
                nivel.menu_activo = False
                nivel.nivel_terminado = False

            if self.rect_play.collidepoint(mouse_pos) and nivel.juego_en_pausa:
                self.sonido(hacia_atras=True)
                nivel.juego_en_pausa = False
                nivel.menu_activo = False
                nivel.nivel_terminado = False
                
            if self.rect_volver_al_menu.collidepoint(mouse_pos):
                self.sonido(hacia_atras=True)
                nivel.nivel = nivel.generar_instancia_nivel()
                nivel.menu_activo = True
                nivel.nivel_terminado = False
                nivel.ingreso_nivel_dos = False
        
        if self.rect_pausa.collidepoint(mouse_pos) or nivel.juego_en_pausa:
            nivel.juego_en_pausa = True
            nivel.nivel_terminado = True


    def sonido(self, hacia_atras=False, canal=None, sonido=None):
        if hacia_atras:
            self.sonidos.canal_efectos.play(self.sonidos.SONIDO_HACIA_ATRAS)
        else:
            canal.play(sonido)
        

    def dibujar_fondo_estrellas(self, personaje, factor_desplazamiento_x, factor_desplazamiento_y, capa):
        fondo_x = -personaje.rect.x * factor_desplazamiento_x * capa
        fondo_y = -personaje.rect.y * factor_desplazamiento_y * capa

        PANTALLA_JUEGO.blit(self.fondo_estrellas, (fondo_x, fondo_y))

    def generar_estrellas(self, radio):
        for _ in range(NUMERO_ESTRELLAS):
            x = random.randint(0, ANCHO_FONDO_ESTRELLAS)
            y = random.randint(0, ALTO_FONDO_ESTRELLAS)
            pygame.draw.circle(self.fondo_estrellas, (255, 255, 255), (x, y), radio)














    # def verificar_colisiones(self, mouse_pos, nivel) -> None:
    #     """
    #     - Se encarga de verificar si hay colisiones entre los objetos.
    #     - Recibe la posicion del mouse.
    #     - No retorna nada
    #     """
    #     # Obtener la posición del personaje y los objetos
    #     for misil in nivel.grupo_misiles:            
    #         if not misil.colision and pygame.sprite.collide_mask(nivel.personaje, misil):
    #             # Sacamos de a una vida si hubo un choque
    #             for vidas in nivel.vidas_personaje:
    #                 vidas.kill()
    #                 break
    #             nivel.vida_personaje -= 1
    #             misil.colision = True
    #         # Si el misil no le esta pegando al personaje, misil.colision vuelve a false.
    #         if not pygame.sprite.collide_mask(nivel.personaje, misil): 
    #             misil.colision = False

    #     for bala_extra in nivel.grupo_balas_extra:
    #         if pygame.sprite.collide_mask(nivel.personaje, bala_extra):
    #             nivel.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
    #             bala_extra.kill()

    #     # Verifico si la bala del personaje le pega al misil
    #     for bala in nivel.grupo_balas_personaje:
    #         for misil in nivel.grupo_misiles:    
    #             if pygame.sprite.collide_mask(bala, misil):
    #                 misil.vida -= 1
    #                 for vida in misil.vidas_misil: # Eliminamos la imagen de la vida del misil al que el personaje impacta con sus balas
    #                     vida.kill()
    #                     break
    #                 # sumamos puntos al matar al misil
    #                 if misil.vida == 0:
    #                     nivel.contador_puntos += PUNTOS_POR_MISIL
    #                 bala.kill()
        
    #     if self.rect_pausa.collidepoint(mouse_pos) or nivel.juego_en_pausa:
    #         nivel.juego_en_pausa = True
    #         nivel.nivel_terminado = True

