
Instalación de la biblioteca **tesserocr**
==========================================

Revisar las indicaciones que se presentan en el [sitio web](https://pypi.python.org/pypi/tesserocr) del paquete de Python. Tener presente que la versión a instalar es la correspondiente a Python3, por lo que se debe usar `pip3` para la instalación. 


Debian Buster
-------------

Al intentar instalar en una máquina con Debian Buster (testing) se presentaron problemas que se solucionaron clonando el repositorio de [tesserocr](https://github.com/sirfz/tesserocr/) e invocando el comando `CPPFLAGS=-std=c++11 pip3 install .` tal como se indica en [este issue](https://github.com/sirfz/tesserocr/issues/26).
