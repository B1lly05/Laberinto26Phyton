from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Norte(Orientacion_Clase):
    def caminar(self, un_bicho):
        elemento_al_norte = un_bicho.posicion.forma.norte
        elemento_al_norte.entrar(un_bicho)

    def poner_elemento(self, un_em, una_forma):
        una_forma.norte = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.norte

    def __str__(self):
        return "Norte"
