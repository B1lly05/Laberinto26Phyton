import threading
from .Contenedor import Habitacion_Clase
from .Hoja import Pared_Clase, Puerta_Clase
from .Orientaciones import Norte, Sur, Este, Oeste
from .Prota import Prota_Clase
from .Decorator import Bomba
from .Laberinto import Laberinto_Clase
class Juego_Clase:
    def __init__(self):
        self.laberinto = None
        self.bichos = []      # Lista para guardar todos los bichos
        self.hilos = {}       # Diccionario para los threads
        self.personaje = None # El protagonista
    # GESTION DE ENTES
    def agregar_personaje(self, nombre):
        self.personaje = Prota_Clase(nombre)
        # Lo metemos por defecto en la habitación 1
        hab1 = self.obtener_habitacion(1)
        hab1.entrar(self.personaje)

    def agregar_bicho(self, un_bicho):
        self.bichos.append(un_bicho)

    def eliminar_bicho(self, un_bicho):
        if un_bicho in self.bichos:
            self.bichos.remove(un_bicho)

    def _lanzar_hilo_bicho(self, un_bicho):
        # Bucle equivalente al block [ ... whileTrue: ... ] de Smalltalk
        while un_bicho.estaVivo():
            un_bicho.actua()
            
        # Si el bucle se rompe es porque ha muerto. Lo eliminamos DEFINITIVAMENTE del juego
        self.eliminar_bicho(un_bicho)
        if un_bicho in self.hilos:
            del self.hilos[un_bicho]

    def lanzar_bicho(self, un_bicho):
        print(f"[{un_bicho}] se activa")
        hilo = threading.Thread(target=self._lanzar_hilo_bicho, args=(un_bicho,), daemon=True)
        self.hilos[un_bicho] = hilo
        hilo.start()

    def lanzar_todos_los_bichos(self):
        print("--- Los bichos despiertan ---")
        for bicho in self.bichos:
            self.lanzar_bicho(bicho)

    def terminar_bicho(self, un_bicho):
        un_bicho.vidas = 0  # Al quitarle las vidas, saldrá del bucle while la próxima vez
        print(f"[{un_bicho}] muere")

    def terminar_todos_los_bichos(self):
        print("--- Se exterminan todos los bichos ---")
        for bicho in self.bichos:
            self.terminar_bicho(bicho)

    # Cosas que usan el iterator
    def abrir_todas_las_puertas(self):
        # Le pasamos la función "accion_abrir" al recorrer
        self.laberinto.recorrer(self.accion_abrir)

    def cerrar_todas_las_puertas(self):
        self.laberinto.recorrer(self.accion_cerrar)

    def activar_todas_las_bombas(self):
        self.laberinto.recorrer(self.accion_activar_bomba)

    def desactivar_todas_las_bombas(self):
        self.laberinto.recorrer(self.accion_desactivar_bomba)


    # FUNCIONES AUXILIARES QUE COMPRUEBAN SI SON O NO EL ELEMNTO QUE BUSCAMOS
    # Estas funciones pueden ir dentro de tu clase Juego o fuera como utilidades
    def accion_abrir(self,elemento):
        if elemento.EsPuerta():
            elemento.abrir_puerta()

    def accion_cerrar(self,elemento):
        if elemento.EsPuerta():
            elemento.cerrar_puerta()

    def accion_activar_bomba(self,elemento):
        if elemento.EsBomba():
            elemento.activar_bomba()

    def accion_desactivar_bomba(self,elemento):
        if elemento.EsBomba():
            elemento.desactivar_bomba()

    #FABRICAR Y GESTIONAR HABITACIONES Y SUS METODOS AUXILIARES. FACTORY METHOD
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fabricar_habitacion(self,numero):      #Metodo que  fabrica una habitacion y le pone paredes y orientaciones, FACTORY METHOD
        # Smalltal: fabricarHabitacion:unNum 
        habitacion = Habitacion_Clase(numero)
        self.asignar_orientaciones(habitacion)
        self.configurar_paredes(habitacion)
        return habitacion
        
    def configurar_paredes(self, hab):          # Metodo auxiliar que usaré en fabricar habitacion para que me ponga paredes en todas las orientaciones
      # Smalltalk: hab orientaciones do:[:each | hab ponerEn:each elemento:self fabricarPared]
      for cada_orientacion in hab.orientaciones:
        # Usamos el método de doble despacho que creamos en la habitación
        hab.poner_en_orientacion(cada_orientacion, self.fabricar_pared())    
        
    def asignar_orientaciones(self, un_cont):
        un_cont.agregar_orientacion(Norte())
        un_cont.agregar_orientacion(Sur())
        un_cont.agregar_orientacion(Este())
        un_cont.agregar_orientacion(Oeste())


    def obtener_habitacion(self,numero):
       return self.laberinto.obtener_habitacion(numero)   
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    # Fabricar cosas
    
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
    
    def fabricar_puerta(self):
        return Puerta_Clase()   
    def fabricar_laberinto(self):
        return Laberinto_Clase()
    def fabricarPuertaLado1Lado2(self,unahb,otrahb):
        puerta = Puerta_Clase(f"Puerta {unahb.num}-{otrahb.num}")
        puerta.lado1 = unahb
        puerta.lado2 = otrahb
        return puerta

    
    #METODOS PARA CREAR LABERINTOS
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    def crear_laberinto_2_habitaciones(self): # La forma normal poniendo las habitaciones de uno en uno
        # Creamos las piezas
        hab1 = Habitacion_Clase(1)
        hab2 = Habitacion_Clase(2)
        puerta = Puerta_Clase("Puerta de Roble")
        
        # Configuramos la puerta
        puerta.lado1 = hab1
        puerta.lado2 = hab2
        puerta.abrir_puerta() # La abrimos para poder pasar
        
        # Habitación 1: Puerta al Este, resto Paredes
        hab1.poner_en_orientacion(Norte(), Pared_Clase())
        hab1.poner_en_orientacion(Sur(), Pared_Clase())
        hab1.poner_en_orientacion(Oeste(), Pared_Clase())
        hab1.poner_en_orientacion(Este(), puerta)
        
        # Habitación 2: Puerta al Oeste, resto Paredes
        hab2.poner_en_orientacion(Norte(), Pared_Clase())
        hab2.poner_en_orientacion(Sur(), Pared_Clase())
        hab2.poner_en_orientacion(Este(), Pared_Clase())
        hab2.poner_en_orientacion(Oeste(), puerta)
        
        self.laberinto = Laberinto_Clase()
        self.laberinto.agregar_hijo(hab1)
        self.laberinto.agregar_hijo(hab2)
        return self.laberinto

    
    def crear_laberinto_2_habitacionesFM(self): # Usando el factory method y sustituir las paredes correspondientes por puertas
        # Uso del Factory Method
        hab1 = self.fabricar_habitacion(1)
        hab2 = self.fabricar_habitacion(2)
    
        # Solo queda conectar lo que es diferente (la puerta)
        puerta = self.fabricarPuertaLado1Lado2(hab1,hab2)
        
        hab1.poner_en_orientacion(Este(), puerta)
        hab2.poner_en_orientacion(Oeste(), puerta)
        self.laberinto = self.fabricar_laberinto()
        self.laberinto.agregar_hijo(hab1)
        self.laberinto.agregar_hijo(hab2)
        return self.laberinto

    def crear_laberinto_4_habitacionesFM(self): # Usando el factory method y sustituir las paredes correspondientes por puertas
        hab1 = self.fabricar_habitacion(1)
        hab2 = self.fabricar_habitacion(2)
        hab3 = self.fabricar_habitacion(3)
        hab4 = self.fabricar_habitacion(4)
        
        puerta12 = self.fabricarPuertaLado1Lado2(hab1,hab2)
        puerta13 = self.fabricarPuertaLado1Lado2(hab1,hab3)
        puerta24 = self.fabricarPuertaLado1Lado2(hab2,hab4)
        puerta34 = self.fabricarPuertaLado1Lado2(hab3,hab4)
        
        hab1.poner_en_orientacion(Sur(),puerta12)
        hab2.poner_en_orientacion(Norte(),puerta12)
        
        hab1.poner_en_orientacion(Este(),puerta13)
        hab3.poner_en_orientacion(Oeste(),puerta13)
        
        hab2.poner_en_orientacion(Este(),puerta24)
        hab4.poner_en_orientacion(Oeste(),puerta24)
        
        hab3.poner_en_orientacion(Sur(),puerta34)
        hab4.poner_en_orientacion(Norte(),puerta34)
        
        self.laberinto = self.fabricar_laberinto()
        self.laberinto.agregar_hijo(hab1)
        self.laberinto.agregar_hijo(hab2)
        self.laberinto.agregar_hijo(hab3)
        self.laberinto.agregar_hijo(hab4)
        
        return self.laberinto
    
    def crear_laberinto_4_habitacionesFMBOMBAS(self):
        self.crear_laberinto_4_habitacionesFM()
        
        hab1 = self.laberinto.obtener_habitacion(1)
        hab3 = self.laberinto.obtener_habitacion(3)
        
        bomba1 = Bomba()
        bomba2 = Bomba()
        
        hab1.agregar_hijo(bomba1)
        hab3.agregar_hijo(bomba2)
        
        return self.laberinto
        