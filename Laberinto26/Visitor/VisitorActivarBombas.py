from Laberinto26.Visitor.Visitor import Visitor_Clase

class VisitorActivarBombas(Visitor_Clase):
    def visitar_bomba(self, bomba):
        bomba.activar_bomba()
