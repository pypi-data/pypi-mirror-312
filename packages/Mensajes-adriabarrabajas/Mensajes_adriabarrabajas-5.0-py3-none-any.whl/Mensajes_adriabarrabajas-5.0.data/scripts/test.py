# Contenido del script "test.py"

# Se importa del paquete "mensajes" el modulo "saludos" del subpaquete "hola"
from mensajes.hola.saludos import *
# Se importa del paquete "mensajes" el modulo "despedidas" del subpaquete "adios"
from mensajes.adios.despedidas import *

# Se carga la función "saludar" del archivo "saludos.py"
saludar()

# Se crea una instancia
saludo = Saludo()

# Se carga la función "despedir" del archivo "despedidas.py"
despedir()

# Se crea una instancia
despido = Despedida()