from Laberinto26.Juego import Juego_Clase
from Laberinto26.ElementosFisicos.Laberinto import Laberinto_Clase
from Laberinto26.ElementosFisicos.Habitacion import Habitacion_Clase
from Laberinto26.ElementosFisicos.Armario import Armario_Clase
from Laberinto26.ElementosFisicos.Pared import Pared_Clase
from Laberinto26.ElementosFisicos.Puerta import Puerta_Clase
from Laberinto26.ElementosFisicos.Bomba import Bomba
from Laberinto26.Orientaciones.Norte import Norte
from Laberinto26.Orientaciones.Sur import Sur
from Laberinto26.Orientaciones.Este import Este
from Laberinto26.Orientaciones.Oeste import Oeste
from Laberinto26.Entidades.Agresivo import Agresivo
from Laberinto26.Entidades.Perezoso import Perezoso
from Laberinto26.Entidades.Guardian import Guardian
from Laberinto26.Entidades.Bicho import Bicho_Clase

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
        
        for cada_orientacion in arm.forma.orientaciones:
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
        if str_modo.lower() == "guardian":
            bicho.nombre = "Guardian del Laberinto"
            bicho.vidas = 250
            bicho.poder = 25

        hab.entrar(bicho)
        self.juego.agregar_bicho(bicho)

    def fabricar_bomba_en(self, un_cont):
        bm = Bomba()
        un_cont.agregar_hijo(bm)

    def fabricar_armario_bomba_veneno_en(self, un_num, un_cont):
        from Laberinto26.ElementosFisicos.ArmarioBombaVeneno import ArmarioBombaVeneno
        arm = ArmarioBombaVeneno(un_num)
        un_cont.agregar_hijo(arm)
        return arm

    def fabricar_bomba_veneno_en(self, un_cont):
        from Laberinto26.ElementosFisicos.BombaVeneno import BombaVeneno
        bm = BombaVeneno()
        un_cont.agregar_hijo(bm)

    def fabricar_este(self):
        return Este()

    def fabricar_habitacion(self, un_num):
        hab = Habitacion_Clase(un_num)
        self.asignar_orientaciones(hab)
        
        for cada_orientacion in hab.forma.orientaciones:
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

    def fabricar_guardian(self):
        return Guardian()

    def fabricar_puerta_lados(self, num1, or_str1, num2, or_str2, estado_str="cerrada"):
        pt = Puerta_Clase(f"Puerta {num1}-{num2}")
        lado1 = self.laberinto.obtener_habitacion(num1)
        lado2 = self.laberinto.obtener_habitacion(num2)
        
        pt.lado1 = lado1
        pt.lado2 = lado2
        
        obj_or1 = getattr(self, f"fabricar_{or_str1.lower()}")()
        obj_or2 = getattr(self, f"fabricar_{or_str2.lower()}")()
        
        lado1.poner_en_orientacion(obj_or1, pt)
        lado2.poner_en_orientacion(obj_or2, pt)
        
        if estado_str == "abierta":
            from Laberinto26.Estados.Abierta import Abierta
            pt.estado = Abierta()

