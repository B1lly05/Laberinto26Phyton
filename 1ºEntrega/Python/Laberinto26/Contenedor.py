import random
from .ElementoMapa import ElementoMapa_Clase
from .Decorator import Bomba

class Contenedor_Clase(ElementoMapa_Clase):
    def __init__(self, num = None):
        super().__init__()

        self.hijos = [] 
        self.orientaciones = []

        self.num = num

        self.este = None
        self.norte = None
        self.oeste = None
        self.sur = None
    
    def poner_en_orientacion(self, orientacion, elemento):
        orientacion.poner_elemento(elemento, self)    
    
    def obtenerOrientacionAleatoria(self):
        return random.choice(self.orientaciones)

    def agregar_hijo(self, elemento_mapa):
        self.hijos.append(elemento_mapa)

    def eliminar_hijo(self, elemento_mapa):
        if elemento_mapa in self.hijos:
            self.hijos.remove(elemento_mapa)

    def agregar_orientacion(self, una_or):
        self.orientaciones.append(una_or)

    def eliminar_orientacion(self, una_or):
        if una_or in self.orientaciones:
            self.orientaciones.remove(una_or)

    def entrar_contenedor(self, alguien):
        print(f"{alguien} está en {self}")
        alguien.posicion = self

    def recorrer(self, UnBloque):
        UnBloque(self)
        for hijo in self.hijos:
            hijo.recorrer(UnBloque)
            
        if self.norte: self.norte.recorrer(UnBloque)
        if self.sur: self.sur.recorrer(UnBloque)
        if self.este: self.este.recorrer(UnBloque)
        if self.oeste: self.oeste.recorrer(UnBloque)


class Habitacion_Clase(Contenedor_Clase):
    def __init__(self, num):
        super().__init__(num)

    def entrar_habitacion(self, alguien):
        print(f"{alguien} ha entrado en la habitación {self.num}")
        alguien.posicion = self
        for cada_hijo in self.hijos: # Metodo que lo que hace es que al entrar a la habitacion, mire sus hijos y si hay una bomba, explote
            # Si el hijo es una Bomba, se ejecutará su método entrar y explotará
            cada_hijo.entrar(alguien)

    def __str__(self):
        return f"Habitación {self.num}"

    def entrar(self, alguien):
        alguien.posicion = self 
        print(f"{alguien} ahora está en la habitación {self.num}")    

class Armario_Clase(Contenedor_Clase):
    def __init__(self,num = None):
        super().__init__(num)

    def __str__(self):
        return f"Armario {self.num}"