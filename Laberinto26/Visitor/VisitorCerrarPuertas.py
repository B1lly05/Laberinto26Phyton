from Laberinto26.Visitor.Visitor import Visitor_Clase

class VisitorCerrarPuertas(Visitor_Clase):
    def visitar_puerta(self, puerta):
        puerta.cerrar_puerta()
