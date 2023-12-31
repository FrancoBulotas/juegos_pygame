import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra
from vida import Vida
from enemigos import Misil
from general_niveles import GeneralNiveles#, Estrella
from utilidades import *
import random

class NivelUno:
    def __init__(self, sonidos) -> None:
        self.fondo = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-uno.png").convert_alpha()
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
        self.ingreso_nivel = False
        self.contador_puntos = 0
        self.contador_eliminaciones = 0

        self.juego_en_pausa = False
        self.flag_archivo_guardado = False
        self.archivo_puntos = obtener_nombre_archivo_puntos(nivel_uno=True)

        self.sonidos = sonidos
        self.sonido_fondo = False
        self.general_nivel = GeneralNiveles(self.personaje, self.sonidos)
        
        self.general_nivel.generar_estrellas(0.5)
        self.general_nivel.generar_estrellas(1)
        self.general_nivel.generar_estrellas(1.5)


    def desarrollo(self, mouse_pos, nivel, cursor, conexion) -> bool:
        """
        - Se encarga de la ejecucion principal del nivel uno.
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

            self.general_nivel.dibujar_barra_superior(self.nivel)    

            # Agregamos municion extra
            self.grupo_balas_extra.update()
            # Actualizamos balas del personaje
            self.grupo_balas_personaje.update()
            # Actualizar y dibujar los misiles, balas y vidas
            self.grupo_misiles.update(self.sonidos)

            for i in range(len(self.vidas_personaje)):
                self.vidas_personaje.update(self.personaje, i)

            self.grupo_misiles.draw(PANTALLA_JUEGO)
            self.grupo_balas_personaje.draw(PANTALLA_JUEGO)
            
            # Actualizar la posición del personaje
            self.personaje.chequeo_teclas(self.sonidos, self.grupo_balas_personaje, self.vida_personaje)

        if self.nivel_terminado:
            if not self.flag_archivo_guardado and not self.juego_en_pausa:
                #self.archivo_puntos = guardar_archivo_puntos(self.nivel.contador_puntos, nivel_uno=True)
                guardar_datos_en_base(self.nivel.contador_puntos, cursor, eliminaciones_misil=self.contador_eliminaciones)
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


    def generar_instancia_nivel(self):
        return NivelUno(self.sonidos)
    

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
        # Obtener la posición del personaje y los objetos
        for misil in self.grupo_misiles:            
            if not misil.colision and pygame.sprite.collide_mask(self.personaje, misil):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1
                #self.sonidos.canal_impactos.play(self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
                self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_A_PERSONAJE)
                misil.colision = True
            # Si el misil no le esta pegando al personaje, misil.colision vuelve a false.
            if not pygame.sprite.collide_mask(self.personaje, misil): 
                misil.colision = False

        for bala_extra in self.grupo_balas_extra:
            if pygame.sprite.collide_mask(self.personaje, bala_extra):
                self.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
                self.general_nivel.sonido(canal=self.sonidos.canal_efectos, sonido=self.sonidos.SONIDO_MUNICION_EXTRA)
                bala_extra.kill()

        # Verifico si la bala del personaje le pega al misil
        for bala in self.grupo_balas_personaje:
            for misil in self.grupo_misiles:    
                if pygame.sprite.collide_mask(bala, misil):
                    misil.vida -= 1
                    for vida in misil.vidas_misil: # Eliminamos la imagen de la vida del misil al que el personaje impacta con sus balas
                        vida.kill()
                        #self.sonidos.canal_impactos.play(self.sonidos.SONIDO_GOLPE_MISIL)
                        self.general_nivel.sonido(canal=self.sonidos.canal_impactos, sonido=self.sonidos.SONIDO_GOLPE_MISIL)
                        break
                    # sumamos puntos al matar al misil
                    if misil.vida == 0:
                        self.contador_eliminaciones += 1
                        self.contador_puntos += PUNTOS_POR_MISIL
                    bala.kill()
        
        # if self.general_nivel.rect_pausa.collidepoint(mouse_pos) or self.juego_en_pausa:
        #     self.juego_en_pausa = True
        #     self.nivel_terminado = True



    # def eleccion_menu_fin(self, mouse_pos):
    #     if pygame.mouse.get_pressed()[0]:
    #         if self.general_nivel.rect_volver_a_jugar.collidepoint(mouse_pos):
    #             self.nivel_tres = NivelTres()
    #             self.menu_activo = False
    #             self.nivel_terminado = False

    #         if self.general_nivel.rect_play.collidepoint(mouse_pos) and self.juego_en_pausa:
    #             self.juego_en_pausa = False
    #             self.menu_activo = False
    #             self.nivel_terminado = False
                
    #         if self.general_nivel.rect_volver_al_menu.collidepoint(mouse_pos):
    #             self.nivel_tres = NivelTres()
    #             self.menu_activo = True
    #             self.nivel_terminado = False
    #             self.ingreso_nivel_tres = False