from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Oeste(Orientacion_Clase):
    def caminar(self, un_bicho):
        elemento_al_oeste = un_bicho.posicion.forma.oeste
        elemento_al_oeste.entrar(un_bicho)

    def poner_elemento(self, un_em, una_forma):
        una_forma.oeste = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.oeste

    def __str__(self):
        return "Oeste"
