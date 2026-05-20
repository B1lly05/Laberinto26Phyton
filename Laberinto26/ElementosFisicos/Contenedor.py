import random
from Laberinto26.ElementosFisicos.ElementoMapa import ElementoMapa_Clase
from Laberinto26.ElementosFisicos.Cuadrado import Cuadrado

class Contenedor_Clase(ElementoMapa_Clase):
    def __init__(self, num = None):
        super().__init__()
        self.hijos = [] 
        self.num = num
        self.forma = Cuadrado()
    
    def poner_en_orientacion(self, orientacion, elemento):
        self.forma.poner_en_orientacion(orientacion, elemento)
    
    def obtener_elemento(self, orientacion):
        return self.forma.obtener_elemento(orientacion)
    
    def obtenerOrientacionAleatoria(self):
        return self.forma.obtener_orientacion_aleatoria()

    def agregar_hijo(self, elemento_mapa):
        self.hijos.append(elemento_mapa)

    def eliminar_hijo(self, elemento_mapa):
        if elemento_mapa in self.hijos:
            self.hijos.remove(elemento_mapa)

    def agregar_orientacion(self, una_or):
        self.forma.agregar_orientacion(una_or)

    def eliminar_orientacion(self, una_or):
        self.forma.eliminar_orientacion(una_or)

    def entrar_contenedor(self, alguien):
        print(f"{alguien} está en {self}")
        alguien.posicion = self

    def aceptar(self, visitor):
        for hijo in self.hijos:
            hijo.aceptar(visitor)
            
        for orientacion in self.forma.orientaciones:
            elemento = self.obtener_elemento(orientacion)
            if elemento:
                elemento.aceptar(visitor)