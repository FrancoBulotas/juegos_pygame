import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra, BalaExtraMejorada
from vida import Vida, VidaExtra
from enemigos import NaveAlien


class NivelTres:
    def __init__(self) -> None:
        self.fondo = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-tres.jpg").convert_alpha()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Crear el personaje
        self.personaje = Personaje()
        self.vida_personaje = self.personaje.vida
        #self.personaje.contador_municion += 10
        # Creamos balas del personaje y alien
        self.grupo_balas_personaje = pygame.sprite.Group()
        self.grupo_balas_personaje_mejoradas = pygame.sprite.Group()

        self.grupo_balas_alien_violeta = pygame.sprite.Group()
        self.grupo_balas_alien_plateado = pygame.sprite.Group()
        # Creamos balas extra
        self.grupo_balas_extra = pygame.sprite.Group()
        for i in range(CANTIDAD_BALAS_EXTRA):
            bala = BalaExtra()
            self.grupo_balas_extra.add(bala)
        
        self.grupo_balas_extra_mejorada = pygame.sprite.Group()
        for i in range(CANTIDAD_BALAS_EXTRA_MEJORADAS):
            bala = BalaExtraMejorada()
            self.grupo_balas_extra_mejorada.add(bala)
        # Generamos el grupo de las vidas
        self.vidas_personaje = pygame.sprite.Group()
        for i in range(VIDAS_PERSONAJE):
            vida = Vida()
            self.vidas_personaje.add(vida)

        self.vidas_extra = pygame.sprite.Group()
        for i in range(CANTIDAD_VIDAS_EXTRA + 2):
            vida_extra = VidaExtra()
            self.vidas_extra.add(vida_extra)

        # Generamos enemigo
        self.nave_alien_violeta = NaveAlien(nivel_dos=True)
        self.nave_alien_plateado = NaveAlien(nivel_tres=True)
        # Variables de estado del juego
        self.cronometro = TIEMPO_NIVEL
        self.cronometro_previo = TIEMPO_NIVEL
        self.intervalo = 1

        self.menu_activo = False
        self.nivel_terminado = False
        self.resultado_ganador = False
        self.ingreso_nivel_tres = False

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png").convert_alpha()
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
        self.juego_en_pausa = False

        self.contador_puntos = 0

    def desarrollo(self, mouse_pos, nivel_tres):
        """
        - Se encarga de la ejecucion principal del nivel dos.
        - No recibe nada.
        - Retorna si el nivel termino o no, y el resultado. (valores booleanos)
        """
        self.nivel_tres = nivel_tres

        self.verificar_colisiones(mouse_pos)

        if not self.juego_en_pausa and not self.nivel_terminado:
            # Chequear variables del estado del juego
            self.chequeo_estado_juego()

            PANTALLA_JUEGO.blit(self.fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
            self.dibujar_barra_superior()    

            # Agregamos municion y vidas extra
            self.grupo_balas_extra.update()
            self.grupo_balas_extra_mejorada.update()
            self.vidas_extra.update()
            # Actualizamos balas del personaje
            self.grupo_balas_personaje.update()
            self.grupo_balas_personaje_mejoradas.update()
            # Actualizar y dibujar los misiles, balas y vidas
            for i in range(len(self.vidas_personaje)):
                self.vidas_personaje.update(self.personaje, i)

            self.grupo_balas_personaje.draw(PANTALLA_JUEGO)
            self.grupo_balas_personaje_mejoradas.draw(PANTALLA_JUEGO)
            
            # Actualizar la posición de personajes
            if self.nave_alien_violeta.vida > 0:
                #self.nave_alien.kill()
                self.nave_alien_violeta.actualizar()
            if self.nave_alien_plateado.vida > 0:
                #self.nave_alien.kill()
                self.nave_alien_plateado.actualizar()
            
            # Creacion balas nave alien
            # tiempo_inicial = TIEMPO_NIVEL
            # if self.cronometro > tiempo_inicial-1:
            #     self.nave_alien.crear_bala(self.grupo_balas_alien, self.personaje)
            if self.cronometro_previo - self.cronometro >= self.intervalo:
                self.nave_alien_violeta.crear_bala(self.grupo_balas_alien_violeta, self.personaje)
                self.nave_alien_plateado.crear_bala(self.grupo_balas_alien_plateado, self.personaje)
                self.cronometro_previo = self.cronometro

            self.grupo_balas_alien_plateado.update()
            self.grupo_balas_alien_plateado.draw(PANTALLA_JUEGO)

            self.grupo_balas_alien_violeta.update()
            self.grupo_balas_alien_violeta.draw(PANTALLA_JUEGO)

            self.personaje.chequeo_teclas(self.grupo_balas_personaje, self.vida_personaje, self.grupo_balas_personaje_mejoradas)


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

        elif self.nave_alien_violeta.vida <= 0 and self.nave_alien_plateado.vida <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = True
        # si se queda sin balas
        elif (self.nave_alien_violeta.vida > 0 or self.nave_alien_plateado.vida > 0) and self.personaje.contador_municion == 0 and len(self.grupo_balas_extra) == 0 and len(self.grupo_balas_personaje) == 0:
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
        # colision entre personaje y nave alien_violeta
        if pygame.sprite.collide_mask(self.personaje, self.nave_alien_violeta) and not self.nave_alien_violeta.colision:
            # Sacamos de a una vida si hubo un choque
            for vidas in self.vidas_personaje:
                vidas.kill()
                break
            self.vida_personaje -= 1
            self.nave_alien_violeta.colision = True
        if not pygame.sprite.collide_mask(self.personaje, self.nave_alien_violeta):
            self.nave_alien_violeta.colision = False

        # colision entre personaje y nave alien_plateada
        if pygame.sprite.collide_mask(self.personaje, self.nave_alien_plateado) and not self.nave_alien_plateado.colision:
            # Sacamos de a una vida si hubo un choque
            for vidas in self.vidas_personaje:
                vidas.kill()
                break
            self.vida_personaje -= 1
            self.nave_alien_plateado.colision = True
        if not pygame.sprite.collide_mask(self.personaje, self.nave_alien_plateado):
            self.nave_alien_plateado.colision = False

        # Colision entre balas alien_violeta con personaje
        for bala in self.grupo_balas_alien_violeta:            
            if not bala.colision and pygame.sprite.collide_mask(self.personaje, bala):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                bala.kill()
                bala.colision = True
            # Si el bala no le esta pegando al personaje, bala.colision vuelve a false.
            if not pygame.sprite.collide_mask(self.personaje, bala): 
                bala.colision = False
        
        # Colision entre balas alien_plateado con personaje
        for bala in self.grupo_balas_alien_plateado:            
            if not bala.colision and pygame.sprite.collide_mask(self.personaje, bala):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                bala.kill()
                bala.colision = True
            # Si el bala no le esta pegando al personaje, bala.colision vuelve a false.
            if not pygame.sprite.collide_mask(self.personaje, bala): 
                bala.colision = False
        
        # Colision con vida extra
        for vida_extra in self.vidas_extra:
            if pygame.sprite.collide_mask(vida_extra, self.personaje):
                self.vida_personaje += 1
                vida_extra.kill()
                vida = Vida()
                self.vidas_personaje.add(vida)

        # Colision entre personaje y balas extra
        for bala_extra in self.grupo_balas_extra:
            if pygame.sprite.collide_mask(self.personaje, bala_extra):
                self.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
                bala_extra.kill()

        for bala_extra_mejorada in self.grupo_balas_extra_mejorada:
            if pygame.sprite.collide_mask(self.personaje, bala_extra_mejorada):
                self.personaje.contador_municion_mejorada += MUNICION_POR_BALAS_EXTRA_MEJORADA
                bala_extra_mejorada.kill()
        # Click en pausa
        if self.rect_pausa.collidepoint(mouse_pos) or self.juego_en_pausa:
            self.juego_en_pausa = True
            self.nivel_terminado = True

        # Verifico si la bala del personaje le pega al alien_violeta y a sus balas
        for bala_personaje in self.grupo_balas_personaje:    
            if pygame.sprite.collide_mask(bala_personaje, self.nave_alien_violeta):
                self.nave_alien_violeta.vida -= 1
                for vida in self.nave_alien_violeta.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    vida.kill()
                    break
                # Puntos por matar nave alien
                if self.nave_alien_violeta.vida == 0:
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                bala_personaje.kill()

            for bala_alien in self.grupo_balas_alien_violeta:
                if pygame.sprite.collide_mask(bala_personaje, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_puntos += PUNTOS_POR_ALIEN
                    bala_personaje.kill()  

        # Verifico si la bala mejorada del personaje le pega al alien_violeta y a sus balas
        for bala_personaje_mejorada in self.grupo_balas_personaje_mejoradas:    
            if pygame.sprite.collide_mask(bala_personaje_mejorada, self.nave_alien_violeta):
                self.nave_alien_violeta.vida -= 2
                cont = 0
                for vida in self.nave_alien_violeta.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    if cont < 2:    
                        vida.kill()
                    cont += 1
                # Puntos por matar nave alien
                if self.nave_alien_violeta.vida == 0:
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                bala_personaje_mejorada.kill()

            for bala_alien in self.grupo_balas_alien_violeta:
                if pygame.sprite.collide_mask(bala_personaje_mejorada, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_puntos += PUNTOS_POR_ALIEN

        # Verifico si la bala del personaje le pega al alien_plateado y a sus balas
        for bala_personaje in self.grupo_balas_personaje:    
            if pygame.sprite.collide_mask(bala_personaje, self.nave_alien_plateado):
                self.nave_alien_plateado.vida -= 1
                for vida in self.nave_alien_plateado.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    vida.kill()
                    break
                # Puntos por matar nave alien
                if self.nave_alien_plateado.vida == 0:
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                bala_personaje.kill()

            for bala_alien in self.grupo_balas_alien_plateado:
                if pygame.sprite.collide_mask(bala_personaje, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_puntos += PUNTOS_POR_ALIEN
                    bala_personaje.kill()  
        
        # Verifico si la bala mejorada del personaje le pega al alien_plateado y a sus balas
        for bala_personaje_mejorada in self.grupo_balas_personaje_mejoradas:    
            if pygame.sprite.collide_mask(bala_personaje_mejorada, self.nave_alien_plateado):
                self.nave_alien_plateado.vida -= 2
                cont = 0
                for vida in self.nave_alien_plateado.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    if cont < 2:    
                        vida.kill()
                    cont += 1
                # Puntos por matar nave alien
                if self.nave_alien_plateado.vida == 0:
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                bala_personaje_mejorada.kill()

            for bala_alien in self.grupo_balas_alien_plateado:
                if pygame.sprite.collide_mask(bala_personaje_mejorada, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_puntos += PUNTOS_POR_ALIEN


    def dibujar_barra_superior(self) -> None:
        """
        - Se encarga de dibujar la barra superior del nivel.
        - No recibe nada.
        - No retorna nada.
        """
        # Parte negra superior
        imagen_superior = pygame.image.load(RECURSOS + "fondo_niveles\\nivel-parte-superior-2.png").convert_alpha()
        imagen_superior = pygame.transform.scale(imagen_superior, (ANCHO_PANTALLA + 300, ALTURA_MENU_SUPERIOR))
        PANTALLA_JUEGO.blit(imagen_superior, (-150, -5))

        imagen_linea = pygame.image.load(RECURSOS + "fondo_niveles\\linea-recta.png").convert_alpha()
        imagen_linea = pygame.transform.scale(imagen_linea, (ANCHO_PANTALLA, 40))
        PANTALLA_JUEGO.blit(imagen_linea, (0, 60))
        # Contador disparos
        fuente = pygame.font.SysFont("Arial Black", 45)
        texto_municion = fuente.render(str(self.personaje.contador_municion), True, (255,255,255))
        PANTALLA_JUEGO.blit(texto_municion, (50, 0))
        imagen_municion = pygame.image.load(RECURSOS + "personaje\\municion.png").convert_alpha()
        PANTALLA_JUEGO.blit(imagen_municion, (10,10))

        texto_municion_mejorada = fuente.render(str(self.personaje.contador_municion_mejorada), True, (255,255,255))
        PANTALLA_JUEGO.blit(texto_municion_mejorada, (210, 0))
        imagen_municion_mejorada = pygame.image.load(RECURSOS + "personaje\\municion-mejorada-extra.png").convert_alpha()
        imagen_municion_mejorada = pygame.transform.scale(imagen_municion_mejorada, (50,50))
        PANTALLA_JUEGO.blit(imagen_municion_mejorada, (150,8))
        # Contador
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
        imagen_fondo_menu =  pygame.image.load(RECURSOS + "menu\\menu-fin.png").convert_alpha()
        imagen_fondo_menu = pygame.transform.scale(imagen_fondo_menu, (600, 600))
        PANTALLA_JUEGO.blit(imagen_fondo_menu, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 300))

        imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\iconos\\repeat.png").convert_alpha()
        rect_volver_a_jugar = imagen_volver_a_jugar.get_rect()
        rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 160
        rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 140                     
        PANTALLA_JUEGO.blit(imagen_volver_a_jugar, rect_volver_a_jugar)

        imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\iconos\\home.png").convert_alpha()
        rect_volver_al_menu = imagen_volver_al_menu.get_rect()
        rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 230 
        rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 140                        
        PANTALLA_JUEGO.blit(imagen_volver_al_menu, rect_volver_al_menu)
        
        # Menu pausado
        imagen_paused = pygame.image.load(RECURSOS + "menu\\paused.png").convert_alpha()
        
        imagen_play = pygame.image.load(RECURSOS + "menu\\iconos\\play.png").convert_alpha()
        rect_play = imagen_play.get_rect()
        rect_play.x = (ANCHO_PANTALLA // 2) - 30
        rect_play.y = ALTO_PANTALLA // 2 + 140
        if self.juego_en_pausa and self.nivel_terminado:            
            PANTALLA_JUEGO.blit(imagen_paused, ((ANCHO_PANTALLA // 2) - 125, ALTO_PANTALLA // 2 - 150))
            PANTALLA_JUEGO.blit(imagen_play, rect_play)

        if self.resultado_ganador and not self.juego_en_pausa:
            imagen_ganador = pygame.image.load(RECURSOS + "menu\\WIN.png").convert_alpha()
            PANTALLA_JUEGO.blit(imagen_ganador, ((ANCHO_PANTALLA // 2) - 170, ALTO_PANTALLA // 2 - 150))

        elif not self.resultado_ganador and not self.juego_en_pausa:
            imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png").convert_alpha()
            PANTALLA_JUEGO.blit(imagen_perdedor, ((ANCHO_PANTALLA // 2) - 270, ALTO_PANTALLA // 2 - 150))

        PANTALLA_JUEGO.blit(self.texto_puntos, ((ANCHO_PANTALLA // 2) - 230, ALTO_PANTALLA // 2 + 10))
        PANTALLA_JUEGO.blit(self.texto_cant_puntos, ((ANCHO_PANTALLA // 2) + 100, ALTO_PANTALLA // 2 + 10))


        if pygame.mouse.get_pressed()[0]:
            if rect_volver_a_jugar.collidepoint(mouse_pos):
                nivel_tres = NivelTres()
                self.menu_activo = False
                self.nivel_terminado = False
                return self.menu_activo, nivel_tres
            
            if rect_play.collidepoint(mouse_pos) and self.juego_en_pausa:
                self.juego_en_pausa = False
                self.menu_activo = False
                self.nivel_terminado = False
                return self.menu_activo, self.nivel_tres
            
            if rect_volver_al_menu.collidepoint(mouse_pos):
                nivel_tres = NivelTres()
                self.menu_activo = True
                self.nivel_terminado = False
                self.ingreso_nivel_tres = False
                return self.menu_activo, nivel_tres