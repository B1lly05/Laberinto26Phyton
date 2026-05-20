from .Ente import Ente_Clase

class Prota_Clase(Ente_Clase):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
    
    def poner_nombre(self, nombre):
        self.nombre = nombre

    def presentarse(self):
        print(f"Nuestro pequeño héroe se llama {self.nombre} tiene {self.vidas} vidas y de de fuerte es en {self.poder} de KI")
        
    def __str__(self):
        return f"{self.nombre}" 


