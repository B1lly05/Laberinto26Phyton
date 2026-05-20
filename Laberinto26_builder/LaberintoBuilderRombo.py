from .LaberintoBuilder import LaberintoBuilder_Clase
from Laberinto26.ElementosFisicos.Habitacion import Habitacion_Clase
from Laberinto26.ElementosFisicos.Armario import Armario_Clase
from Laberinto26.ElementosFisicos.Rombo import Rombo
from Laberinto26.Orientaciones.Noreste import Noreste
from Laberinto26.Orientaciones.Noroeste import Noroeste
from Laberinto26.Orientaciones.Sureste import Sureste
from Laberinto26.Orientaciones.Suroeste import Suroeste

class LaberintoBuilderRombo_Clase(LaberintoBuilder_Clase):
    def __init__(self):
        super().__init__()

    def asignar_orientaciones(self, un_cont):
        un_cont.agregar_orientacion(self.fabricar_noreste())
        un_cont.agregar_orientacion(self.fabricar_noroeste())
        un_cont.agregar_orientacion(self.fabricar_sureste())
        un_cont.agregar_orientacion(self.fabricar_suroeste())

    def fabricar_habitacion(self, un_num):
        hab = Habitacion_Clase(un_num)
        hab.forma = Rombo()  # Asignamos la forma geométrica de rombo
        self.asignar_orientaciones(hab)
        
        for cada_orientacion in hab.forma.orientaciones:
            hab.poner_en_orientacion(cada_orientacion, self.fabricar_pared())
            
        self.laberinto.agregar_hijo(hab)
        
        return hab

    def fabricar_armario_en(self, un_num, un_cont):
        arm = Armario_Clase(un_num)
        arm.forma = Rombo()
        self.asignar_orientaciones(arm)
        
        for cada_orientacion in arm.forma.orientaciones:
            arm.poner_en_orientacion(cada_orientacion, self.fabricar_pared())
            
        # Como no hay Este ni Oeste, usaremos sureste para la puerta por defecto en los armarios de rombo
        from Laberinto26.ElementosFisicos.Puerta import Puerta_Clase
        pt = Puerta_Clase(f"Puerta Armario {un_num}")
        pt.lado1 = arm
        pt.lado2 = un_cont
        
        arm.poner_en_orientacion(self.fabricar_sureste(), pt)
        
        un_cont.agregar_hijo(arm)
        
        return arm

    # --- Fábricas de orientaciones diagonales ---
    def fabricar_noreste(self):
        return Noreste()

    def fabricar_noroeste(self):
        return Noroeste()

    def fabricar_sureste(self):
        return Sureste()

    def fabricar_suroeste(self):
        return Suroeste()
