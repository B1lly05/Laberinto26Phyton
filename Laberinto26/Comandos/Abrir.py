from Laberinto26.Comandos.Comando import Comando_Clase

class Abrir(Comando_Clase):
    def __init__(self, receptor=None):
        super().__init__(receptor)

    def ejecutar(self, alguien=None):
        if self.receptor:
            self.receptor.abrir_puerta()
