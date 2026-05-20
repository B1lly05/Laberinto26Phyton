from Laberinto26.Comandos.Comando import Comando_Clase

class AtacarComando(Comando_Clase):
    def __init__(self, interfaz):
        super().__init__(interfaz)

    def ejecutar(self, alguien=None):
        self.receptor._realizar_ataque()
