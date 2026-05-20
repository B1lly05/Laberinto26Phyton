import time
from Laberinto26.Entidades.Modo import Modo_Clase

class Perezoso(Modo_Clase):
    def duerme(self, un_bicho):
        print(f"{un_bicho} duerme mucho (5 segundos)")
        time.sleep(3)

    def esPerezoso(self):
        return True

    def __str__(self):
        return "Perezoso"
