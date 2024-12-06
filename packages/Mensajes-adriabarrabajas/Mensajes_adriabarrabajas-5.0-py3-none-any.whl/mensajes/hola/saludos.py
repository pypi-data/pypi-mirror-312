# Se importa el módulo "numpy"
import numpy as np

# Se define la función "saludar"
def saludar():
    # que devuelva este mensaje desde la función saludar contenida en el fichero saludos
    print("Hola, te saludo desde saludos.saludar()")

# Se define otra función "prueba"
def prueba():
    # que devuelva este mensaje
    print("Esto es una prueba de la nueva versión")

# Se define otra función "generar_array" que llame a "numpy" para generar un array con tantos números como se le indiquen
def generar_array(numeros):
    return np.arange(numeros)

# Se crea una clase
class Saludo:
    # Se define el método constructor
    def __init__(self):
        # Que devuelva el siguiente mensaje
        print("Hola, te saludo desde Saludo.__init__")


# Para evitar ejecutar un código de un módulo desde otro fichero se puede utilizar una comprobación que devuelve el nombre en clave
# se puede utilizar una comprobación que devuelve el nombre en clave del fichero mientras se está ejecutando
if __name__ == '__main__':
# Se llama a la función
    print(generar_array(5))