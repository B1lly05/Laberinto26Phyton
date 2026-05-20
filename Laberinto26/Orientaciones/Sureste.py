from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Sureste(Orientacion_Clase):
    def poner_elemento(self, un_em, una_forma):
        una_forma.sureste = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.sureste

    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.sureste
        em.entrar(un_bicho)
