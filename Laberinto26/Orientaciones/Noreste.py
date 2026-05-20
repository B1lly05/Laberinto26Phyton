from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Noreste(Orientacion_Clase):
    def poner_elemento(self, un_em, una_forma):
        una_forma.noreste = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.noreste

    def caminar(self, un_bicho):
        em = un_bicho.posicion.forma.noreste
        em.entrar(un_bicho)
