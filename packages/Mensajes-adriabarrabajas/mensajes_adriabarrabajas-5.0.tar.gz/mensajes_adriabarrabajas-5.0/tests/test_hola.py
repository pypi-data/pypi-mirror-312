# Contenido del script "test_hola.py"

# Se importa el módulo "unittest"
import unittest
# Se importa el módulo "numpy"
import numpy as np
# Se importa la función "generar_array"
from mensajes.hola.saludos import generar_array

# Se crea una clase "PruebasHola" con las pruebas unitest correspondientes
class PruebasHola(unittest.TestCase):
    # Se define una prueba
    def test_generar_array(self):
        # Se ejecuta el módulo testing.assert_array_equal de la librería "numpy"
        np.testing.assert_array_equal(
            # Se genera el array de los 6 elementos y se realiza la prueba para ver si se ejecuta la prueba correctamente
            np.array([0,1,2,3,4,5]),
            generar_array(np.array(6))
        )