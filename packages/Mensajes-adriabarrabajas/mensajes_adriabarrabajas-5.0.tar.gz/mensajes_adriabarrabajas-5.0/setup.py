# Contenido del script "setup.py"

# Se importa la función setup de la biblioteca setuptools
# Se importa la función find_packages de la biblioteca setuptools
from setuptools import setup, find_packages

# Se llama a esta función con una serie de parámetros
setup(
    name = 'Mensajes-adriabarrabajas', # nombre del paquete
    version = '5.0', # version
    description = 'Un paquete para saludar y despedir', # descripción
    long_description = open('README.md').read(), # descripción larga,
    long_description_content_type='text/markdown', # tipo de fichero que se carga en long_description
    author = 'Hectór Costa Guzmán', # autor
    author_email = 'hola@hektor.dev', # correo del autor
    url = 'https://www.hektor.dev', # dirección web
    packages = find_packages(), # lista de paquetes
    scripts = ['test.py'], # lista de scripts a incluir en el paquete distribuible
    test_suite = 'tests', # se indica
    install_requires = [paquete.strip() # lista de librerías que se deben instalar previamente con el número de versión
                         for paquete in open ("requirements.txt").readlines()],
    classifiers=[ # clasificadores seleccionados
        'Environment :: Console', # entorno
        'Intended Audience :: Developers', # audiencia
        'License :: OSI Approved :: MIT License', # licencia
        'Operating System :: OS Independent', # sistema operativo
        'Programming Language :: Python', # lenguaje
        'Programming Language :: Python :: 3.9', # version
        'Programming Language :: Python :: 3.10', # otra version
        'Topic :: Utilities' # utilidades
    ]
)