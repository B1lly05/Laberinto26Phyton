from .Ente import Ente_Clase

class Bicho_Clase(Ente_Clase):
    def __init__(self, modo=None, nombre="Bicho Anónimo"):
        super().__init__() 
        self.modo = modo
        self.nombre = nombre
    def actua(self):
        if self.modo is not None:
            self.modo.actua(self)

    def esAgresivo(self):
        if self.modo is not None:
            return self.modo.esAgresivo()
        return False

    def esPerezoso(self):
        if self.modo is not None:
            return self.modo.esPerezoso()
        return False

    def __str__(self):
        return f"{self.nombre} [{self.modo}]"