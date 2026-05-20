from Laberinto26.Estados.EstadoEnte import EstadoEnte_Clase

class Muerto(EstadoEnte_Clase):
    def estaVivo(self):
        return False
