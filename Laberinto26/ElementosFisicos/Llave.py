from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class Llave(Hoja_Clase):
    def __init__(self):
        super().__init__()

    def EsLlave(self):
        return True

    def entrar(self, alguien):
        print(f"{alguien} ha encontrado una llave.")
