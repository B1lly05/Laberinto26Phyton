import time

class Modo_Clase:
    def actua(self, un_bicho):
        self.camina(un_bicho)
        if un_bicho.estaVivo():
            self.duerme(un_bicho)

    def camina(self, un_bicho):
        if un_bicho.posicion is not None:
            orien = un_bicho.posicion.obtenerOrientacionAleatoria()
            if orien is not None:
                orien.caminar(un_bicho)

    def esAgresivo(self):
        return False

    def esPerezoso(self):
        return False

    def esGuardian(self):
        return False