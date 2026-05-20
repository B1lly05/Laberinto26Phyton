from Laberinto26.ElementosFisicos.Forma import Forma_Clase

class Cuadrado(Forma_Clase):
    def __init__(self):
        super().__init__()
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
