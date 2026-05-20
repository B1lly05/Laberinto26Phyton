from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Noroeste(Orientacion_Clase):
    def poner_elemento(self, un_em, una_forma):
        una_forma.noroeste = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.noroeste

    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.noroeste
        em.entrar(un_bicho)
