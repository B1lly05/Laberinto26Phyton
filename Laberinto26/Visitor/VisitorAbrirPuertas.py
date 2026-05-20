from Laberinto26.Visitor.Visitor import Visitor_Clase

class VisitorAbrirPuertas(Visitor_Clase):
    def visitar_puerta(self, puerta):
        puerta.abrir_puerta()
