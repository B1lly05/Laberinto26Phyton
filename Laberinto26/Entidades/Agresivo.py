import time
from Laberinto26.Entidades.Modo import Modo_Clase

class Agresivo(Modo_Clase):
    def duerme(self, un_bicho):
        print(f"{un_bicho} apenas duerme (1 segundo) por su agresividad")
        time.sleep(1)

    def esAgresivo(self):
        return True

    def __str__(self):
        return "Agresivo"
