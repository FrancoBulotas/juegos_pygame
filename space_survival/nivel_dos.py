import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra
from vida import Vida, VidaExtra
from enemigos import NaveAlien, Misil
from general_niveles import GeneralNiveles
from utilidades import *

class NivelDos:
    def __init__(self) -> None:
        self.fondo = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-dos.jpg").convert_alpha()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Crear el personaje
        self.personaje = Personaje()
        self.vida_personaje = self.personaje.vida
        # Creamos balas del personaje y alien
        self.grupo_balas_personaje = pygame.sprite.Group()
        self.grupo_balas_alien = pygame.sprite.Group()
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

        self.vidas_extra = pygame.sprite.Group()
        for i in range(CANTIDAD_VIDAS_EXTRA):
            vida_extra = VidaExtra()
            self.vidas_extra.add(vida_extra)

        # Generamos enemigo
        self.nave_alien = NaveAlien(nivel_dos=True)
        self.grupo_asteroides = pygame.sprite.Group()
        # Variables de estado del juego
        self.cronometro = TIEMPO_NIVEL
        self.cronometro_previo_nave = TIEMPO_NIVEL
        self.cronometro_previo_misiles = TIEMPO_NIVEL
        self.intervalo_para_nave = 1
        self.intervalo_para_asteroides = 3

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
        self.archivo_puntos = obtener_nombre_archivo_puntos(nivel_dos=True)
        self.general_nivel = GeneralNiveles(self.personaje)


    def desarrollo(self, mouse_pos, nivel, sonidos, cursor, conexion):
        """
        - Se encarga de la ejecucion principal del nivel dos.
        - No recibe nada.
        - Retorna si el nivel termino o no, y el resultado. (valores booleanos)
        """
        self.nivel = nivel
        self.verificar_colisiones(sonidos)
        self.general_nivel.eleccion_menu_fin(sonidos, mouse_pos, self.nivel)

        if not self.juego_en_pausa and not self.nivel_terminado:
 
            # Chequear variables del estado del juego
            self.chequeo_estado_juego()

            PANTALLA_JUEGO.blit(self.fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
            self.general_nivel.dibujar_barra_superior(self.nivel)    

            # Agregamos municion y vidas extra
            self.grupo_balas_extra.update()
            self.vidas_extra.update()
            # Actualizamos balas del personaje
            self.grupo_balas_personaje.update()
            # Actualizar y dibujar los misiles, balas y vidas
            for i in range(len(self.vidas_personaje)):
                self.vidas_personaje.update(self.personaje, i)

            #self.grupo_misiles.draw(PANTALLA_JUEGO)
            self.grupo_balas_personaje.draw(PANTALLA_JUEGO)
            
            # Actualizar la posición de personajes
            if self.nave_alien.vida > 0:
                #self.nave_alien.kill()
                self.nave_alien.actualizar(sonidos)

            # Chequeo los intervalos
            if self.cronometro_previo_nave - self.cronometro >= self.intervalo_para_nave:
                self.nave_alien.crear_bala(self.grupo_balas_alien, self.personaje)
                self.cronometro_previo_nave = self.cronometro

            if self.cronometro_previo_misiles - self.cronometro >= self.intervalo_para_asteroides:
                misil = Misil(nivel_dos=True)
                self.grupo_asteroides.add(misil)
                self.cronometro_previo_misiles = self.cronometro

            self.grupo_balas_alien.update(sonidos)
            self.grupo_balas_alien.draw(PANTALLA_JUEGO)

            self.grupo_asteroides.update(sonidos)
            self.grupo_asteroides.draw(PANTALLA_JUEGO)

            self.personaje.chequeo_teclas(sonidos, self.grupo_balas_personaje, self.vida_personaje)
        
        if self.nivel_terminado:
            if not self.flag_archivo_guardado:
                #self.archivo_puntos = guardar_archivo_puntos(nivel.contador_puntos, nivel_dos=True)
                guardar_puntos_en_base(self.nivel.contador_puntos, cursor, eliminaciones_alien=self.contador_eliminaciones_aliens, eliminaciones_nave_alien=self.contador_eliminaciones_naves)
                conexion.commit()
                self.flag_archivo_guardado = True

            self.general_nivel.dibujar_menu_fin(self.nivel, sonidos)
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

        elif self.nave_alien.vida <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = True
        # si se queda sin balas
        elif self.nave_alien.vida > 0 and self.personaje.contador_municion == 0 and len(self.grupo_balas_extra) == 0 and len(self.grupo_balas_personaje) == 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = False
    
        elif self.cronometro <= 0:
            self.nivel_terminado = True
            self.cronometro = 0
            self.resultado_ganador = False

    def generar_instancia_nivel(self):
        return NivelDos()

    def verificar_colisiones(self, sonidos) -> None:
        """
        - Se encarga de verificar si hay colisiones entre los objetos.
        - Recibe la instancia del sonido.
        - No retorna nada
        """
        # colision entre personaje y nave alien
        if pygame.sprite.collide_mask(self.personaje, self.nave_alien) and not self.nave_alien.colision:
            # Sacamos de a una vida si hubo un choque
            for vidas in self.vidas_personaje:
                vidas.kill()
                break
            self.vida_personaje -= 1
            self.nave_alien.colision = True
        if not pygame.sprite.collide_mask(self.personaje, self.nave_alien):
            self.nave_alien.colision = False

        # Colision entre balas alien con personaje
        for bala in self.grupo_balas_alien:            
            if not bala.colision and pygame.sprite.collide_mask(self.personaje, bala):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                bala.colision = True
                bala.kill()
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

        # Verifico si la bala del personaje le pega a la nave y a sus balas
        for bala_personaje in self.grupo_balas_personaje:    
            if pygame.sprite.collide_mask(bala_personaje, self.nave_alien):
                self.nave_alien.vida -= 1
                for vida in self.nave_alien.vidas_nave: # Eliminamos la imagen de la vida de la nave 
                    vida.kill()
                    break
                # Puntos por matar nave alien
                if self.nave_alien.vida == 0:
                    self.contador_eliminaciones_naves += 1
                    self.contador_puntos += PUNTOS_POR_NAVE_ALIEN
                sonidos.SONIDO_GOLPE_MISIL.play()
                bala_personaje.kill()

            for bala_alien in self.grupo_balas_alien:
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

        # Colision con asteroide
        for asteroide in self.grupo_asteroides:
            if not asteroide.colision and pygame.sprite.collide_mask(self.personaje, asteroide):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                asteroide.colision = True
            # Si el asteroide no le esta pegando al personaje, asteroide.colision vuelve a false.
            if not pygame.sprite.collide_mask(self.personaje, asteroide): 
                asteroide.colision = False
