from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class EspadaOlimpo(Hoja_Clase):
    def __init__(self):
        super().__init__()

    def EsEspadaOlimpo(self):
        return True

    def entrar(self, alguien):
        print(f"{alguien} ha encontrado la Espada del Olimpo.")
