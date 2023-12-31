import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra, BalaExtraMejorada
from vida import Vida, VidaExtra
from enemigos import NaveAlien
from general_niveles import GeneralNiveles
from utilidades import *


class NivelTres:
    def __init__(self, sonidos) -> None:
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
        self.ingreso_nivel = False

        self.imagen_pausa = pygame.image.load(RECURSOS + "menu\\iconos\\pause.png").convert_alpha()
        self.imagen_pausa = pygame.transform.scale(self.imagen_pausa,(40,40))
        self.rect_pausa = self.imagen_pausa.get_rect()
        self.juego_en_pausa = False

        self.contador_puntos = 0
        self.contador_eliminaciones_naves = 0
        self.contador_eliminaciones_aliens = 0

        self.flag_archivo_guardado = False
        self.archivo_puntos = obtener_nombre_archivo_puntos(nivel_tres=True)
        self.sonidos = sonidos
        self.sonido_fondo = False
        self.general_nivel = GeneralNiveles(self.personaje, self.sonidos)
        
        self.general_nivel.generar_estrellas(0.5)
        self.general_nivel.generar_estrellas(1)
        self.general_nivel.generar_estrellas(1.5)

    def desarrollo(self, mouse_pos, nivel, cursor, conexion):
        """
        - Se encarga de la ejecucion principal del nivel dos.
        - No recibe nada.
        - Retorna si el nivel termino o no, y el resultado. (valores booleanos)
        """
        self.nivel = nivel
        self.correr_musica()
        self.verificar_colisiones()
        self.general_nivel.eleccion_menu_fin(mouse_pos, self.nivel)

        if not self.juego_en_pausa and not self.nivel_terminado:
            # Chequear variables del estado del juego
            self.chequeo_estado_juego()

            #PANTALLA_JUEGO.blit(self.fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
            PANTALLA_JUEGO.fill((0,0,0))
            self.general_nivel.dibujar_fondo_estrellas(self.personaje, 0.1, 0.1, capa=1)
            self.general_nivel.dibujar_fondo_estrellas(self.personaje, 0.1, 0.1, capa=2)
            self.general_nivel.dibujar_fondo_estrellas(self.personaje, 0.1, 0.1, capa=3)

            self.general_nivel.dibujar_barra_superior(self.nivel, nivel_tres=True)    

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
            if self.nave_alien_violeta.vida >= 0:
                self.nave_alien_violeta.actualizar(self.sonidos)
            if self.nave_alien_plateado.vida >= 0:
                self.nave_alien_plateado.actualizar(self.sonidos)
            
            # Creacion balas nave alien
            if self.cronometro_previo - self.cronometro >= self.intervalo:
                self.nave_alien_violeta.crear_bala(self.grupo_balas_alien_violeta, self.personaje)
                self.nave_alien_plateado.crear_bala(self.grupo_balas_alien_plateado, self.personaje)
                self.cronometro_previo = self.cronometro

            self.grupo_balas_alien_plateado.update(self.sonidos)
            self.grupo_balas_alien_plateado.draw(PANTALLA_JUEGO)

            self.grupo_balas_alien_violeta.update(self.sonidos)
            self.grupo_balas_alien_violeta.draw(PANTALLA_JUEGO)

            self.personaje.chequeo_teclas(self.sonidos, self.grupo_balas_personaje, self.vida_personaje, self.grupo_balas_personaje_mejoradas)

        if self.nivel_terminado:
            if not self.flag_archivo_guardado and not self.juego_en_pausa:
                #self.archivo_puntos = guardar_archivo_puntos(nivel.contador_puntos, nivel_tres=True)
                guardar_datos_en_base(self.nivel.contador_puntos, cursor, eliminaciones_alien=self.contador_eliminaciones_aliens, eliminaciones_nave_alien=self.contador_eliminaciones_naves)
                conexion.commit()
                self.flag_archivo_guardado = True

            self.general_nivel.dibujar_menu_fin(self.nivel, self.sonidos)
            # Esto es para que se pueda volver a jugar dandole a volver a jugar
            self.nivel.ingreso_nivel = True


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

    def generar_instancia_nivel(self):
        return NivelTres(self.sonidos)
    
    def correr_musica(self):
        if not self.sonido_fondo:
            self.sonidos.canal_fondo.play(self.sonidos.SONIDO_FONDO_NIVEL)
            self.sonido_fondo = True


    def verificar_colisiones(self) -> None:
        """
        - Se encarga de verificar si hay colisiones entre los objetos.
        - Recibe la instancia del sonido.
        - No retorna nada
        """
        # colision entre personaje y nave alien_violeta
        if pygame.sprite.collide_mask(self.personaje, self.nave_alien_violeta) and not self.nave_alien_violeta.colision:
            # Sacamos de a una vida si hubo un choque
            for vidas in self.vidas_personaje:
                vidas.kill()
                break
            self.vida_personaje -= 1
            self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
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
            self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
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
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
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
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
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
                self.general_nivel.sonido(canal=self.sonidos.canal_efectos, sonido=self.sonidos.SONIDO_VIDA_EXTRA)

        # Colision entre personaje y balas extra
        for bala_extra in self.grupo_balas_extra:
            if pygame.sprite.collide_mask(self.personaje, bala_extra):
                self.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
                bala_extra.kill()
                self.general_nivel.sonido(canal=self.sonidos.canal_efectos, sonido=self.sonidos.SONIDO_MUNICION_EXTRA)

        for bala_extra_mejorada in self.grupo_balas_extra_mejorada:
            if pygame.sprite.collide_mask(self.personaje, bala_extra_mejorada):
                self.personaje.contador_municion_mejorada += MUNICION_POR_BALAS_EXTRA_MEJORADA
                bala_extra_mejorada.kill()
                self.general_nivel.sonido(canal=self.sonidos.canal_efectos, sonido=self.sonidos.SONIDO_MUNICION_EXTRA)

        # Verifico si la bala del personaje le pega al alien_violeta y a sus balas
        for bala_personaje in self.grupo_balas_personaje:    
            if pygame.sprite.collide_mask(bala_personaje, self.nave_alien_violeta):
                self.nave_alien_violeta.vida -= 1
                for vida in self.nave_alien_violeta.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    vida.kill()
                    break
                # Puntos por matar nave alien
                if self.nave_alien_violeta.vida == 0:
                    self.contador_eliminaciones_naves += 1
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL)
                bala_personaje.kill()

            for bala_alien in self.grupo_balas_alien_violeta:
                if pygame.sprite.collide_mask(bala_personaje, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_eliminaciones_aliens += 1
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
                    self.contador_eliminaciones_naves += 1
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                    self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL_MEJORADO)
                bala_personaje_mejorada.kill()

            for bala_alien in self.grupo_balas_alien_violeta:
                if pygame.sprite.collide_mask(bala_personaje_mejorada, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_eliminaciones_aliens += 1
                        self.contador_puntos += PUNTOS_POR_ALIEN
                    self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL_MEJORADO)

        # Verifico si la bala del personaje le pega al alien_plateado y a sus balas
        for bala_personaje in self.grupo_balas_personaje:    
            if pygame.sprite.collide_mask(bala_personaje, self.nave_alien_plateado):
                self.nave_alien_plateado.vida -= 1
                for vida in self.nave_alien_plateado.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    vida.kill()
                    break
                # Puntos por matar nave alien
                if self.nave_alien_plateado.vida == 0:
                    self.contador_eliminaciones_naves += 1
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL)
                bala_personaje.kill()

            for bala_alien in self.grupo_balas_alien_plateado:
                if pygame.sprite.collide_mask(bala_personaje, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_eliminaciones_aliens += 1
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
                    self.contador_eliminaciones_naves += 1
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL_MEJORADO)
                bala_personaje_mejorada.kill()

            for bala_alien in self.grupo_balas_alien_plateado:
                if pygame.sprite.collide_mask(bala_personaje_mejorada, bala_alien):
                    bala_alien.vida -= 1
                    for vida in bala_alien.vidas_misil: # Eliminamos la imagen de la vida de la bala del alien 
                        vida.kill()
                        break
                    # Puntos por matar alien
                    if bala_alien.vida == 0:
                        self.contador_eliminaciones_aliens += 1
                        self.contador_puntos += PUNTOS_POR_ALIEN
                    self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL_MEJORADO)
