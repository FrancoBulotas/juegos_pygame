import pygame
from constantes import *
from pygame.locals import *
from personaje import Personaje, BalaExtra
from vida import Vida
from enemigos import Enemigo


class NivelUno:
    def __init__(self) -> None:
        self.fondo = pygame.image.load(RECURSOS + "fondo_niveles\\fondo-nivel-uno3.png")
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Crear el personaje
        self.personaje = Personaje()
        self.vida_personaje = self.personaje.vida
        # Creamos balas del personaje
        self.grupo_balas = pygame.sprite.Group()
        # Creamos balas extra
        self.grupo_balas_extra = pygame.sprite.Group()
        for i in range(CANTIDAD_BALAS_EXTRA_NIVEL_UNO):
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
            misil = Enemigo()
            self.grupo_misiles.add(misil)
        # Variables de estado del juego
        self.cronometro = TIEMPO_NIVEL_UNO
        self.nivel_terminado = False
        self.resultado_ganador = False


    def desarrollo(self) -> bool:
        """
        - Se encarga de la ejecucion principal del nivel uno.
        - No recibe nada.
        - Retorna si el nivel termino o no, y el resultado. (valores booleanos)
        """
        # Verificar colisiones
        self.verificar_colisiones()
        
        PANTALLA_JUEGO.blit(self.fondo, (0, ALTURA_MENU_SUPERIOR - 10)) # Fondo de pantalla
        self.dibujar_barra_superior()    
        # Actualizar la posición del personaje
        self.personaje.chequeo_teclas(self.grupo_balas)
        # Agregamos municion extra
        self.grupo_balas_extra.update()

        # Chequear variables del estado del juego
        self.nivel_terminado, self.cronometro, self.resultado_ganador = self.chequeo_estado_juego()
        if  self.nivel_terminado:
            return  self.nivel_terminado, self.resultado_ganador
        
        # Actualizar y dibujar los misiles, balas y vidas
        for i in range(2):
            self.grupo_misiles.update(self.grupo_balas)
        self.grupo_balas.update()        

        for i in range(len(self.vidas_personaje)):
            self.vidas_personaje.update(self.personaje, i)

        self.grupo_misiles.draw(PANTALLA_JUEGO)
        self.grupo_balas.draw(PANTALLA_JUEGO)
        
        PANTALLA_JUEGO.blit(self.personaje.imagen_nave, self.personaje.rect_nave) # Dibuja la imagen del personaje

            # nivel_terminado, resultado_ganador
        return self.nivel_terminado, self.resultado_ganador

    def chequeo_estado_juego(self) -> bool and int:
        """
        - Se encarga de verificar si el nivel termino o no en base a vida, cantidad de enemigos, municion y tiempo.
        - No recibe nada.
        - Retorna si el nivel termino o no(bool), el cronometro(int) y el resultado(bool).
        """
        # Verificar el número de vidas del personaje
        if self.vida_personaje <= 0:
                # nivel_terminado, cronometro, resultado_ganador 
            return True, 0, False
        elif len(self.grupo_misiles) <= 0:
            # Unica forma de ganar
            return True, 0, True
        # si se queda sin balas
        elif len(self.grupo_misiles) > 0 and (self.personaje.contador_municion == 0 and len(self.grupo_balas_extra) == 0):
            return True, 0, False
        elif self.cronometro < 0:
            return True, 0, False

        return False, self.cronometro, self.resultado_ganador


    def verificar_colisiones(self) -> None:
        """
        - Se encarga de verificar si hay colisiones entre los objetos.
        - No recibe nada.
        - No retorna nada
        """
        # Obtener la posición del personaje y los objetos
        posicion_personaje = self.personaje.rect_nave

        # Verificar colisiones entre el personaje y los misiles
        for misil in self.grupo_misiles:
            posicion_misil = misil.rect
            # Si misil.colision es False, y el misil esta chocando con el personaje entra.
            if not misil.colision and posicion_personaje.colliderect(posicion_misil):
                # Sacamos de a una vida si hubo un choque
                for vidas in self.vidas_personaje:
                    vidas.kill()
                    break
                self.vida_personaje -= 1

                misil.colision = True
            # Si el misil no le esta pegando al personaje, misil.colision vuelve a false.
            if not posicion_personaje.colliderect(posicion_misil): 
                misil.colision = False

        # Verificar colisiones entre personaje y balas extra
        for bala_extra in self.grupo_balas_extra:
            if posicion_personaje.colliderect(bala_extra.rect):
                self.personaje.contador_municion += MUNICION_POR_BALAS_EXTRA
                bala_extra.kill()


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
        # Contador
        texto_crono = fuente.render(str(self.cronometro), True, (255,255,255))
        PANTALLA_JUEGO.blit(texto_crono, (ANCHO_PANTALLA/2, 0))


    def menu_fin(self, mouse_pos):
        """
        - Se encarga de dibujar el resultado del nivel, y de verificar si clickea volver a jugar o ir al menu.
        - Recibe la posicion del mouse.
        - Retorna si el menu esta activo(bool), si el nivel termino(bool) y la instacia del nivel uno creada nuevamente.
        """
        imagen_volver_a_jugar = pygame.image.load(RECURSOS + "menu\\repeat.png")
        rect_volver_a_jugar = imagen_volver_a_jugar.get_rect()
        rect_volver_a_jugar.x = (ANCHO_PANTALLA // 2) + 170
        rect_volver_a_jugar.y = (ALTO_PANTALLA // 2) + 80                        
        PANTALLA_JUEGO.blit(imagen_volver_a_jugar, rect_volver_a_jugar)

        imagen_volver_al_menu = pygame.image.load(RECURSOS + "menu\\home.png")
        rect_volver_al_menu = imagen_volver_al_menu.get_rect()
        rect_volver_al_menu.x = (ANCHO_PANTALLA // 2) - 300 
        rect_volver_al_menu.y = (ALTO_PANTALLA // 2) + 80                        
        PANTALLA_JUEGO.blit(imagen_volver_al_menu, rect_volver_al_menu)
        
        if self.resultado_ganador:
            imagen_ganador = pygame.image.load(RECURSOS + "menu\\WINNER.png")
            PANTALLA_JUEGO.blit(imagen_ganador, ((ANCHO_PANTALLA // 2) - 350, ALTO_PANTALLA // 2 - 80))
        else:
            imagen_perdedor = pygame.image.load(RECURSOS + "menu\\LOSER.png")
            PANTALLA_JUEGO.blit(imagen_perdedor, ((ANCHO_PANTALLA // 2) - 300, ALTO_PANTALLA // 2 - 80))

        if pygame.mouse.get_pressed()[0]:
            if rect_volver_a_jugar.collidepoint(mouse_pos):
                nivel_uno = NivelUno()
                #    menu_activo, nivel_terminado
                return False, False, nivel_uno
            
            if rect_volver_al_menu.collidepoint(mouse_pos):
                nivel_uno = NivelUno()
                #    menu_activo, nivel_terminado
                return True, False, nivel_uno

    