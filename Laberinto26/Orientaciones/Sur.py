from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Sur(Orientacion_Clase):
    def caminar(self, un_bicho):
        elemento_al_sur = un_bicho.posicion.forma.sur
        elemento_al_sur.entrar(un_bicho)

    def poner_elemento(self, un_em, una_forma):
        una_forma.sur = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.sur

    def __str__(self):
        return "Sur"
