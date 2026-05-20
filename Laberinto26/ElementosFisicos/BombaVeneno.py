from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class BombaVeneno(Hoja_Clase):
    def __init__(self):
        super().__init__()
        self.activa = True

    def EsBombaVeneno(self):
        return True

    def EsBomba(self):
        return True

    def activar_bomba(self):
        self.activa = True

    def desactivar_bomba(self):
        self.activa = False

    def entrar(self, alguien):
        if self.activa:
            print(f"¡BOMBA DE VENENO! {alguien} ha pisado una trampa de veneno.")
            alguien.vidas = max(0, alguien.vidas - 15)
            self.activa = False
        else:
            print(f"{alguien} ha pasado cerca de una bomba de veneno inactiva.")

    def aceptar(self, visitor):
        if hasattr(visitor, "visitar_bomba_veneno"):
            visitor.visitar_bomba_veneno(self)
        elif hasattr(visitor, "visitar_bomba"):
            visitor.visitar_bomba(self)
        else:
            super().aceptar(visitor)
