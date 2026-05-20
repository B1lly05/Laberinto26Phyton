from Laberinto26.Visitor.Visitor import Visitor_Clase

class VisitorDesactivarBombas(Visitor_Clase):
    def visitar_bomba(self, bomba):
        bomba.desactivar_bomba()
