import time

class Modo_Clase:
    def actua(self, un_bicho):
        self.camina(un_bicho)
        # Si al caminar pisó una bomba y murió, abortamos antes de que se ponga a dormir
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
    



class Agresivo(Modo_Clase):
    def duerme(self, un_bicho):
        print(f"{un_bicho} apenas duerme (1 segundo) por su agresividad")
        time.sleep(1)

    def esAgresivo(self):
        return True

    def __str__(self):
        return "Agresivo"


class Perezoso(Modo_Clase):
    def duerme(self, un_bicho):
        print(f"{un_bicho} duerme mucho (5 segundos)")
        time.sleep(3)

    def esPerezoso(self):
        return True

    def __str__(self):
        return "Perezoso"    