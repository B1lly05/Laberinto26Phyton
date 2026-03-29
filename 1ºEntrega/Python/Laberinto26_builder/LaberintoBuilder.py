from Laberinto26.Juego import Juego_Clase
from Laberinto26.Laberinto import Laberinto_Clase
from Laberinto26.Contenedor import Habitacion_Clase, Armario_Clase
from Laberinto26.Hoja import Pared_Clase, Puerta_Clase
from Laberinto26.Decorator import Bomba
from Laberinto26.Orientaciones import Norte, Sur, Este, Oeste
from Laberinto26.Modo import Agresivo, Perezoso
from Laberinto26.Bicho import Bicho_Clase

class LaberintoBuilder_Clase:
    def __init__(self):
        self.laberinto = None
        self.juego = None

    def asignar_orientaciones(self, un_cont):
        un_cont.agregar_orientacion(self.fabricar_norte())
        un_cont.agregar_orientacion(self.fabricar_este())
        un_cont.agregar_orientacion(self.fabricar_sur())
        un_cont.agregar_orientacion(self.fabricar_oeste())

    def fabricar_agresivo(self):
        return Agresivo()

    def fabricar_armario_en(self, un_num, un_cont):
        arm = Armario_Clase(un_num)
        self.asignar_orientaciones(arm)
        
        for cada_orientacion in arm.orientaciones:
            arm.poner_en_orientacion(cada_orientacion, self.fabricar_pared())
            
        pt = Puerta_Clase(f"Puerta Armario {un_num}")
        pt.lado1 = arm
        pt.lado2 = un_cont
        
        arm.poner_en_orientacion(self.fabricar_este(), pt)
        
        un_cont.agregar_hijo(arm)
        
        return arm

    def fabricar_bicho_modo_posicion(self, str_modo, un_num):
        metodo_fabricar = getattr(self, f"fabricar_{str_modo.lower()}")
        modo = metodo_fabricar()
        
        hab = self.juego.obtener_habitacion(un_num)
        if hab is None:
            print(f"Error: La habitación {un_num} no existe para colocar el bicho.")
            return

        bicho = Bicho_Clase(modo=modo, nombre=f"Bicho {str_modo}")
        hab.entrar(bicho)
        
        self.juego.agregar_bicho(bicho)

    def fabricar_bomba_en(self, un_cont):
        bm = Bomba()
        un_cont.agregar_hijo(bm)

    def fabricar_este(self):
        return Este()

    def fabricar_habitacion(self, un_num):
        hab = Habitacion_Clase(un_num)
        self.asignar_orientaciones(hab)
        
        for cada_orientacion in hab.orientaciones:
            hab.poner_en_orientacion(cada_orientacion, self.fabricar_pared())
            
        self.laberinto.agregar_hijo(hab)
        
        return hab

    def fabricar_juego(self):
        self.juego = Juego_Clase()
        self.juego.laberinto = self.laberinto

    def fabricar_laberinto(self):
        self.laberinto = Laberinto_Clase()

    def fabricar_norte(self):
        return Norte()
    
    def fabricar_sur(self):
        return Sur()

    def fabricar_este(self):
        return Este()
    def fabricar_oeste(self):
        return Oeste()

    def fabricar_pared(self):
        return Pared_Clase()

    def fabricar_perezoso(self):
        return Perezoso()

    def fabricar_puerta_lados(self, num1, or_str1, num2, or_str2):
        pt = Puerta_Clase(f"Puerta {num1}-{num2}")
        lado1 = self.laberinto.obtener_habitacion(num1)
        lado2 = self.laberinto.obtener_habitacion(num2)
        
        pt.lado1 = lado1
        pt.lado2 = lado2
        
        obj_or1 = getattr(self, f"fabricar_{or_str1.lower()}")()
        obj_or2 = getattr(self, f"fabricar_{or_str2.lower()}")()
        
        lado1.poner_en_orientacion(obj_or1, pt)
        lado2.poner_en_orientacion(obj_or2, pt)

