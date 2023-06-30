import os
import pygame
from constantes import *
import sqlite3

RECURSOS = "recursos\\"

# -------------------------------ARCHIVOS---------------------------------------------
def guardar_archivo_puntos(contador_puntos, nivel_uno=False, nivel_dos=False, nivel_tres=False):
    directorio_actual = os.getcwd()
    ruta_relativa = os.path.join(directorio_actual)
    nombre_archivo = ""
    if nivel_uno:
        nombre_archivo = "puntos_lvl_1.txt"
    elif nivel_dos:
        nombre_archivo = "puntos_lvl_2.txt"
    elif nivel_tres:
        nombre_archivo = "puntos_lvl_3.txt"
    
    with open(ruta_relativa + "\\recursos\\" + nombre_archivo, "a") as archivo_puntuacion:
        archivo_puntuacion.write(str(contador_puntos)+"\n")

    return archivo_puntuacion.name

def leer_archivo_puntos(nombre_archivo):
    lista_puntos=[]
    try:
        with open(nombre_archivo, "r") as archivo_puntos:
            for puntos in archivo_puntos:
                lista_puntos.append(int(puntos))
            return max(lista_puntos)
    except FileNotFoundError:
        return 0
    

def obtener_nombre_archivo_puntos(nivel_uno=False, nivel_dos=False, nivel_tres=False):
    directorio_actual = os.getcwd()
    ruta_relativa = os.path.join(directorio_actual)

    nombre_archivo = ""
    if nivel_uno:
        nombre_archivo = "puntos_lvl_1.txt"
    elif nivel_dos:
        nombre_archivo = "puntos_lvl_2.txt"
    elif nivel_tres:
        nombre_archivo = "puntos_lvl_3.txt"

    return (ruta_relativa + "\\recursos\\" + nombre_archivo)


def guardar_archivo_volumen(volumen):
    directorio_actual = os.getcwd()
    ruta_relativa = os.path.join(directorio_actual)
    
    with open(ruta_relativa + "\\recursos\\volumen.txt", "a") as archivo_puntuacion:
        archivo_puntuacion.write(str(volumen)+"\n")


def leer_archivo_volumen():
    directorio_actual = os.getcwd()
    ruta_relativa = os.path.join(directorio_actual)
    lista_volumen = []
    try:
        with open(ruta_relativa + "\\recursos\\volumen.txt", "r") as archivo_volumen:
            for volumen in archivo_volumen:
                lista_volumen.append(float(volumen))
            return lista_volumen[-1]
    except FileNotFoundError:
        return 0.1
    

# -------------------------------SONIDOS-------------------------------------
pygame.mixer.init()
def generar_sonido(ruta: str, volumen: float):
    '''
    Función que se encarga de generar un sondi
    Recibe la ruta en donde se encuentra ese sonido y el volumen del mismo
    Retorna el sonido para esperar a que se ejecute
    '''
    sonido = pygame.mixer.Sound(ruta)
    sonido.set_volume(volumen)
    return sonido


class Sonidos:
    def __init__(self, volumen) -> None:
            self.volumen = volumen
            self.SONIDO_INICIAR_NIVEL = generar_sonido(RECURSOS + "sonidos\\menu\\start_button.wav", self.volumen) # 1 
            self.SONIDO_HACIA_ATRAS = generar_sonido(RECURSOS + "sonidos\\menu\\back1.wav", self.volumen) # 0.1
            self.SONIDO_FONDO_MENU = generar_sonido(RECURSOS + "sonidos\\musica-fondo-menu.wav", self.volumen) # 0.03
            self.SONIDO_DISPARO_PERSONAJE = generar_sonido(RECURSOS + "sonidos\\switch_to_fire_bomb.wav", self.volumen) # 0.08
            self.SONIDO_DISPARO_PERSONAJE_MEJORADO = generar_sonido(RECURSOS + "sonidos\\rocket_h3_3.wav", self.volumen) # 0.08
            self.SONIDO_EXPLOSION_MISIL = generar_sonido(RECURSOS + "sonidos\\h3_small_expl4.wav", self.volumen) # 0.08
            self.SONIDO_GOLPE_MISIL = generar_sonido(RECURSOS + "sonidos\\rocket_expl_lod_far1.wav", self.volumen) # 0.08
            self.SONIDO_GOLPE_MISIL_MEJORADO = generar_sonido(RECURSOS + "sonidos\\rocket_launcher_lod_far3.wav", self.volumen) # 0.08
            self.SONIDO_EXPLOSION_NAVE = generar_sonido(RECURSOS + "sonidos\\big_explosions3.wav", self.volumen) # 0.03
            self.fuente_volumen = pygame.font.SysFont("Txt_IV25", 30)
            self.texto_volumen = self.fuente_volumen.render("Vol: " + str(round(self.volumen * 10, 1)), True, (255,255,255))

    def regular_volumen(self, sube=False, baja=False):
        if self.volumen >= 0:
            if sube:    
                self.volumen += 0.01
            if baja:
                self.volumen -= 0.01
                if self.volumen <= 0:
                    self.volumen = 0

        self.cambio_volumen(self.volumen)

    def cambio_volumen(self, volumen):
        self.SONIDO_INICIAR_NIVEL.set_volume(volumen)
        self.SONIDO_HACIA_ATRAS.set_volume(volumen)
        self.SONIDO_FONDO_MENU.set_volume(volumen)
        self.SONIDO_DISPARO_PERSONAJE.set_volume(volumen)
        self.SONIDO_DISPARO_PERSONAJE_MEJORADO.set_volume(volumen)
        self.SONIDO_EXPLOSION_MISIL.set_volume(volumen)
        self.SONIDO_GOLPE_MISIL.set_volume(volumen)
        self.SONIDO_GOLPE_MISIL_MEJORADO.set_volume(volumen)
        self.SONIDO_EXPLOSION_NAVE.set_volume(volumen)

        self.texto_volumen = self.fuente_volumen.render("Vol: " + str(round(self.volumen * 10, 1)), True, (255,255,255))

# ---------------------------BASE DE DATOS---------------------------------------
def crear_base_y_cursor(nivel):
    if nivel == 1:
        conexion = sqlite3.connect('base-puntuacion-uno.db')
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS puntuacion
                         (puntos INTEGER)''')
        return conexion, cursor
    if nivel == 2:
        conexion = sqlite3.connect('base-puntuacion-dos.db')
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS puntuacion
                         (puntos INTEGER)''')
        return conexion, cursor
    if nivel == 3:
        conexion = sqlite3.connect('base-puntuacion-tres.db')
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS puntuacion
                         (puntos INTEGER)''')
        return conexion, cursor


def guardar_puntos_en_base(puntos, cursor, conexion):    
    cursor.execute("INSERT INTO puntuacion (puntos) VALUES (?)", (puntos,))
    conexion.commit()


def borrar_datos_base(cursor, conexion):
    for i in range(40):
        i += 1
        cursor.execute("DELETE FROM puntuacion WHERE id = ?", (i,))
        conexion.commit()


def traer_puntos_maximos_de_base(cursor):
    cursor.execute("SELECT MAX(puntos) FROM puntuacion")
    return cursor.fetchone()[0]


def printear_tabla_base(cursor):
    cursor.execute("SELECT * FROM puntuacion")

    filas = cursor.fetchall()
    for fila in filas:
        print(fila) 
