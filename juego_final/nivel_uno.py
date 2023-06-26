import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra
from vida import Vida
from enemigos import Misil
from niveles import MenuNivel


class NivelUno:
    def __init__(self) -> None:
        self.fondo = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-uno.png")
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Crear el personaje
        self.personaje = Personaje()
        self.vida_personaje = self.personaje.vida
        self.personaje.velocidad -= 1
        # Creamos balas del personaje
        self.grupo_balas_personaje = pygame.sprite.Group()
        # Creamos balas extra
        self.grupo_balas_extra = pygame.sprite.Group()
        for i in range(CANTIDAD_BALAS_EXTRA):
            bala = BalaExtra()
            self.grupo_balas_extra.add(bala)

        # Generamos el grupo de las vidas
        self.vidas_personaje = pygame.sprite.Group()
        for i in range(VIDAS_PERSONAJE):
            vida = Vida()
            self.vidas_personaje.add(vida)

        # Crear un grupo para todos los misiles
        self.grupo_misiles = pygame.sprite.Group()
        # Crear misiles
        for i in range(CANTIDAD_MISILES_NIVEL_UN0):
            misil = Misil()
            self.grupo_misiles.add(misil)
        # Variables de estado del juego
        self.cronometro = TIEMPO_NIVEL
        self.menu_activo = False
        self.nivel_terminado = False
        self.resultado_ganador = False
        self.ingreso_nivel_uno = False
        self.contador_puntos = 0

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png")
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
        self.juego_en_pausa = False

        #self.menu_nivel = MenuNivel(self.personaje)
        

    def desarrollo(self, mouse_pos, nivel_uno) -> bool:
        """
        - Se encarga de la ejecucion principal del nivel uno.
        - No recibe nada.
        - Retorna si el nivel termino o no, y el resultado. (valores booleanos)
        """
        self.nivel_uno = nivel_uno

        self.verificar_colisiones(mouse_pos)
        
        if not self.juego_en_pausa and not self.nivel_terminado:
            
            # Chequear variables del estado del juego
            self.chequeo_estado_juego()

            PANTALLA_JUEGO.blit(self.fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
            self.dibujar_barra_superior()    

            # Agregamos municion extra
            self.grupo_balas_extra.update()
            # Actualizamos balas del personaje
            self.grupo_balas_personaje.update()
            # Actualizar y dibujar los misiles, balas y vidas
             
            self.grupo_misiles.update()

            for i in range(len(self.vidas_personaje)):
                self.vidas_personaje.update(self.personaje, i)

            self.grupo_misiles.draw(PANTALLA_JUEGO)
            self.grupo_balas_personaje.draw(PANTALLA_JUEGO)
            
            # Actualizar la posición del personaje
            self.personaje.chequeo_teclas(self.grupo_balas_personaje, self.vida_personaje)
            
            #return self.menu_activo, nivel_uno

        # elif self.nivel_terminado:
        #     try:
        #         self.menu_nivel.menu_fin(self.juego_en_pausa, self.nivel_terminado, self.resultado_ganador)
        #         menu_activo, nivel_uno = self.eleccion_menu_fin(mouse_pos)
        #         # Esto es para que se pueda volver a jugar dandole a volver a jugar
        #         self.ingreso_nivel_uno = True
        #         return menu_activo, nivel_uno
        #     except TypeError:
        #         self.nivel_terminado = True
        #         self.menu_activo = False
        #         return self.menu_activo, nivel_uno


    def chequeo_estado_juego(self) -> None:
        """
        - Se encarga de verificar si el nivel termino o no en base a vida, cantidad de enemigos, municion y tiempo.
        - No recibe nada.
        - No retorna nada.
        """
        # Verificar el número de vidas del personaje
        if self.vida_personaje <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = False

        elif len(self.grupo_misiles) <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = True

        # si se queda sin balas
        elif len(self.grupo_misiles) > 0 and self.personaje.contador_municion == 0 and len(self.grupo_balas_extra) == 0 and len(self.grupo_balas_personaje) == 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = False
            
        elif self.cronometro <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = False


    def verificar_colisiones(self, mouse_pos) -> None:
        """
        - Se encarga de verificar si hay colisiones entre los objetos.
        - Recibe la posicion del mouse.
        - No retorna nada
        """
        # Obtener la posición del personaje y los objetos
        for misil in self.grupo_misiles:            
            if not misil.colision and pygame.sprite.collide_mask(self.personaje, misil):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                misil.colision = True
            # Si el misil no le esta pegando al personaje, misil.colision vuelve a false.
            if not pygame.sprite.collide_mask(self.personaje, misil): 
                misil.colision = False

        for bala_extra in self.grupo_balas_extra:
            if pygame.sprite.collide_mask(self.personaje, bala_extra):
                self.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
                bala_extra.kill()

        #if pygame.mouse.get_pressed()[0]:
        if self.rect_pausa.collidepoint(mouse_pos) or self.juego_en_pausa:
            self.juego_en_pausa = True
            self.nivel_terminado = True

        # Verifico si la bala del personaje le pega al misil
        for bala in self.grupo_balas_personaje:
            for misil in self.grupo_misiles:    
                if pygame.sprite.collide_mask(bala, misil):
                    misil.vida -= 1
                    for vida in misil.vidas_misil: # Eliminamos la imagen de la vida del misil al que el personaje impacta con sus balas
                        vida.kill()
                        break
                    # sumamos puntos al matar al misil
                    if misil.vida == 0:
                        self.contador_puntos += PUNTOS_POR_MISIL
                    bala.kill()


    # def eleccion_menu_fin(self, mouse_pos):
    #     if pygame.mouse.get_pressed()[0]:
    #         if self.menu_nivel.rect_volver_a_jugar.collidepoint(mouse_pos):
    #             nivel_uno = NivelUno()
    #             self.menu_activo = False
    #             self.nivel_terminado = False
    #             return self.menu_activo, nivel_uno
            
    #         if self.menu_nivel.rect_play.collidepoint(mouse_pos) and self.juego_en_pausa:
    #             self.juego_en_pausa = False
    #             self.menu_activo = False
    #             self.nivel_terminado = False
    #             return self.menu_activo, self.nivel_uno
            
    #         if self.menu_nivel.rect_volver_al_menu.collidepoint(mouse_pos):
    #             nivel_uno = NivelUno()
    #             self.menu_activo = True
    #             self.nivel_terminado = False
    #             self.ingreso_nivel_uno = False
    #             return self.menu_activo, nivel_uno

    def dibujar_barra_superior(self) -> None:
        """
        - Se encarga de dibujar la barra superior del nivel.
        - No recibe nada.
        - No retorna nada.
        """
        # Parte negra superior
        imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png")
        imagen_superior = pygame.transform.scale(imagen_superior, (ANCHO_PANTALLA + 300, ALTURA_MENU_SUPERIOR))
        PANTALLA_JUEGO.blit(imagen_superior, (-150, -5))

        imagen_linea = pygame.image.load(RECURSOS + "fondo_niveles\\linea-recta.png")
        imagen_linea = pygame.transform.scale(imagen_linea, (ANCHO_PANTALLA, 40))
        PANTALLA_JUEGO.blit(imagen_linea, (0, 60))
        # Contador disparos
        fuente = pygame.font.SysFont("Arial Black", 45)
        texto_municion = fuente.render(str(self.personaje.contador_municion), True, (255,255,255))
        PANTALLA_JUEGO.blit(texto_municion, (50, 0))
        imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png")
        PANTALLA_JUEGO.blit(imagen_municion, (10,10))
        # Contador tiempo
        texto_crono = fuente.render(str(self.cronometro), True, (255,255,255))
        PANTALLA_JUEGO.blit(texto_crono, (ANCHO_PANTALLA/2, 0))
        # Contador puntos
        self.texto_puntos = fuente.render("Total Points ", True, (255,255,255))
        self.texto_cant_puntos = fuente.render(str(self.contador_puntos), True, (255,255,255))
        PANTALLA_JUEGO.blit(self.texto_cant_puntos, (ANCHO_PANTALLA/2 - 400, 0))

        self.rect_pausa.x = ANCHO_PANTALLA - 50
        self.rect_pausa.y = 10
        PANTALLA_JUEGO.blit(self.imagen_pausa, self.rect_pausa)


    def menu_fin(self, mouse_pos):
        """
        - Se encarga de dibujar el resultado del nivel, y de verificar si clickea volver a jugar o ir al menu.
        - Recibe la posicion del mouse.
        - Retorna si el menu esta activo(bool), si el nivel termino(bool) y la instacia del nivel uno creada nuevamente.
        """
        imagen_fondo_menu =  pygame.image.load(RECURSOS + "menu\\menu-fin.png")
        imagen_fondo_menu = pygame.transform.scale(imagen_fondo_menu, (600, 600))
        PANTALLA_JUEGO.blit(imagen_fondo_menu, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 300))

        imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\iconos\\repeat.png")
        rect_volver_a_jugar = imagen_volver_a_jugar.get_rect()
        rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 160
        rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 140                     
        PANTALLA_JUEGO.blit(imagen_volver_a_jugar, rect_volver_a_jugar)

        imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\iconos\\home.png")
        rect_volver_al_menu = imagen_volver_al_menu.get_rect()
        rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 230 
        rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 140                        
        PANTALLA_JUEGO.blit(imagen_volver_al_menu, rect_volver_al_menu)
        
        # Menu pausado
        imagen_paused = pygame.image.load(RECURSOS + "menu\\paused.png")
        
        imagen_play = pygame.image.load(RECURSOS + "menu\\iconos\\play.png")
        rect_play = imagen_play.get_rect()
        rect_play.x = (ANCHO_PANTALLA // 2) - 30
        rect_play.y = ALTO_PANTALLA // 2 + 140
        if self.juego_en_pausa and self.nivel_terminado:          
            PANTALLA_JUEGO.blit(imagen_paused, ((ANCHO_PANTALLA // 2) - 125, ALTO_PANTALLA // 2 - 150))  
            PANTALLA_JUEGO.blit(imagen_play, rect_play)


        if self.resultado_ganador and not self.juego_en_pausa:
            PANTALLA_JUEGO.blit(self.texto_puntos, ((ANCHO_PANTALLA // 2) - 230, ALTO_PANTALLA // 2 + 10))
            PANTALLA_JUEGO.blit(self.texto_cant_puntos, ((ANCHO_PANTALLA // 2) + 100, ALTO_PANTALLA // 2 + 10))
            imagen_ganador = pygame.image.load(RECURSOS + "menu\\WIN.png")
            PANTALLA_JUEGO.blit(imagen_ganador, ((ANCHO_PANTALLA // 2) - 170, ALTO_PANTALLA // 2 - 150))

        elif not self.resultado_ganador and not self.juego_en_pausa:
            imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png")
            PANTALLA_JUEGO.blit(imagen_perdedor, ((ANCHO_PANTALLA // 2) - 270, ALTO_PANTALLA // 2 - 150))


        if pygame.mouse.get_pressed()[0]:
            if rect_volver_a_jugar.collidepoint(mouse_pos):
                nivel_uno = NivelUno()
                self.menu_activo = False
                self.nivel_terminado = False
                return self.menu_activo, nivel_uno
            
            if rect_play.collidepoint(mouse_pos) and self.juego_en_pausa:
                self.juego_en_pausa = False
                self.menu_activo = False
                self.nivel_terminado = False
                return self.menu_activo, self.nivel_uno
            
            if rect_volver_al_menu.collidepoint(mouse_pos):
                nivel_uno = NivelUno()
                self.menu_activo = True
                self.nivel_terminado = False
                self.ingreso_nivel_uno = False
                return self.menu_activo, nivel_uno
            
