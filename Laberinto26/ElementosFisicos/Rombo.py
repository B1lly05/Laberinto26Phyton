from Laberinto26.ElementosFisicos.Forma import Forma_Clase

class Rombo(Forma_Clase):
    def __init__(self):
        super().__init__()
        self.noreste = None
        self.noroeste = None
        self.sureste = None
        self.suroeste = None
