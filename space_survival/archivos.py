import os


def guardar_archivo(contador_puntos, nivel_uno=False, nivel_dos=False, nivel_tres=False):
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


def leer_archivo(nombre_archivo):
    lista_puntos=[]
    try:
        with open(nombre_archivo, "r") as archivo_puntos:
            for puntos in archivo_puntos:
                lista_puntos.append(int(puntos))
            return max(lista_puntos)
    except FileNotFoundError:
        return 0


def obtener_nombre_archivo(nivel_uno=False, nivel_dos=False, nivel_tres=False):
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