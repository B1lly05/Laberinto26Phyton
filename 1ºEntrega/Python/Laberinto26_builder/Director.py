from Laberinto26.Modo import Agresivo

class Director_Clase:
    def __init__(self):
        self.diccionario = None
        self.builder = None

    def procesar(self, un_diccionario, un_builder):
        self.diccionario = un_diccionario
        self.builder = un_builder
        
        self.builder.fabricar_laberinto()
        self.builder.fabricar_juego()
        
        if "laberinto" in self.diccionario:
            for habitacion_json in self.diccionario["laberinto"]:
                self.procesar_habitacion(habitacion_json)
                
        if "puertas" in self.diccionario:
            for puerta_json in self.diccionario["puertas"]:
                id_hab1 = puerta_json[0]
                orient1 = puerta_json[1]
                id_hab2 = puerta_json[2]
                orient2 = puerta_json[3]
                
                self.builder.fabricar_puerta_lados(id_hab1, orient1, id_hab2, orient2)
                
        if "bichos" in self.diccionario:
            for bicho_json in self.diccionario["bichos"]:
                # El formato es ["Agresivo", 1]
                modo = bicho_json[0]
                posicion = bicho_json[1]
                self.builder.fabricar_bicho_modo_posicion(modo, posicion)

        return self.builder.juego

    def procesar_habitacion(self, dict_hab):
        numero = dict_hab["num"]
        habitacion = self.builder.fabricar_habitacion(numero)
        
        if "hijos" in dict_hab:
            for hijo_json in dict_hab["hijos"]:
                self.procesar_hijos(hijo_json, habitacion)

    def procesar_hijos(self, json_hijo, contenedor_padre):
        tipo = json_hijo.get("tipo")
        
        if tipo == "armario":
            num_armario = json_hijo.get("num")
            armario_creado = self.builder.fabricar_armario_en(num_armario, contenedor_padre)
            
            if "hijos" in json_hijo:
                for sub_hijo in json_hijo["hijos"]:
                    self.procesar_hijos(sub_hijo, armario_creado)
                    
        elif tipo == "bomba":
            self.builder.fabricar_bomba_en(contenedor_padre)
