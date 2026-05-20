import random

class Forma_Clase:
    def __init__(self):
        self.orientaciones = []

    def agregar_orientacion(self, orien):
        self.orientaciones.append(orien)

    def eliminar_orientacion(self, orien):
        if orien in self.orientaciones:
            self.orientaciones.remove(orien)

    def obtener_orientacion_aleatoria(self):
        if self.orientaciones:
            return random.choice(self.orientaciones)
        return None

    def poner_en_orientacion(self, orientacion, elemento):
        orientacion.poner_elemento(elemento, self)

    def obtener_elemento(self, orientacion):
        return orientacion.obtener_elemento(self)
