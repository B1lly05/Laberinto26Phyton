from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class PocionSalud(Hoja_Clase):
    def __init__(self):
        super().__init__()

    def EsPocionSalud(self):
        return True

    def entrar(self, alguien):
        print(f"{alguien} ha encontrado una poción de salud.")
