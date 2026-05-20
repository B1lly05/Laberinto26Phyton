from Laberinto26.Orientaciones.Orientacion import Orientacion_Clase

class Este(Orientacion_Clase):
    def caminar(self, un_bicho):
        elemento_al_este = un_bicho.posicion.forma.este
        elemento_al_este.entrar(un_bicho)

    def poner_elemento(self, un_em, una_forma):
        una_forma.este = un_em

    def obtener_elemento(self, una_forma):
        return una_forma.este

    def __str__(self):
        return "Este"
