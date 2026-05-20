class Ente_Clase():
    def __init__(self):
        self.poder = 10
        self.posicion = None
        self.vidas = 50

    def estaVivo(self):
        return self.vidas > 0
     