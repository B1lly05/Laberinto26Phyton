from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class ArmarioBombaVeneno(Hoja_Clase):
    def __init__(self, num=None):
        super().__init__()
        self.num = num
        self.abierto = False
        self.activa = True

    def EsArmarioBombaVeneno(self):
        return True

    def entrar(self, alguien):
        print(f"{alguien} está frente al Armario Bomba de Veneno {self.num}.")

    def aceptar(self, visitor):
        if hasattr(visitor, "visitar_armario_bomba_veneno"):
            visitor.visitar_armario_bomba_veneno(self)
        else:
            super().aceptar(visitor)
