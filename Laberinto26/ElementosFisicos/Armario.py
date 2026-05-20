from Laberinto26.ElementosFisicos.Contenedor import Contenedor_Clase

class Armario_Clase(Contenedor_Clase):
    def __init__(self,num = None):
        super().__init__(num)

    def __str__(self):
        return f"Armario {self.num}"
