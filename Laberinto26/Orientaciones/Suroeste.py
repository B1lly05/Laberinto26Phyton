from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Suroeste(Orientacion_Clase):
    def poner_elemento(self, un_em, una_forma):
        una_forma.suroeste = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.suroeste

    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.suroeste
        em.entrar(un_bicho)
