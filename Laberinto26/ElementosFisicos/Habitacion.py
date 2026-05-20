from Laberinto26.ElementosFisicos.Contenedor import Contenedor_Clase

class Habitacion_Clase(Contenedor_Clase):
    def __init__(self, num):
        super().__init__(num)

    def entrar_habitacion(self, alguien):
        print(f"{alguien} ha entrado en la habitación {self.num}")
        alguien.posicion = self
        for cada_hijo in self.hijos: 
            cada_hijo.entrar(alguien)

    def __str__(self):
        return f"Habitación {self.num}"

    def entrar(self, alguien):
        alguien.posicion = self 
        print(f"{alguien} ahora está en la habitación {self.num}")    

    def aceptar(self, visitor):
        visitor.visitar_habitacion(self)
        super().aceptar(visitor)
