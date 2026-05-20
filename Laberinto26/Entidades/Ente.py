from Laberinto26.Estados.Vivo import Vivo
from Laberinto26.Estados.Muerto import Muerto

class Ente_Clase():
    def __init__(self):
        self.poder = 10
        self.posicion = None
        self.estado = Vivo()
        self._vidas = 50

    @property
    def vidas(self):
        return self._vidas

    @vidas.setter
    def vidas(self, valor):
        self._vidas = max(0, valor)
        if self._vidas == 0:
            self.estado = Muerto()
        else:
            self.estado = Vivo()

    def estaVivo(self):
        return self.estado.estaVivo()
     