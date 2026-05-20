import sys
import os
# Añadir la raíz del proyecto al path: funciona tanto ejecutado directamente como importado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

# Configuramos la consola a UTF-8 para que soporte los Emojis de forma segura
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import json
from Laberinto26_builder.LaberintoBuilder import LaberintoBuilder_Clase
from Laberinto26_builder.Director import Director_Clase
from Laberinto26.Orientaciones.Este import Este
from Laberinto26.Orientaciones.Norte import Norte
from Laberinto26.Orientaciones.Oeste import Oeste
from Laberinto26.Orientaciones.Sur import Sur

class VistaLaberinto_Clase:
    _instancia = None

    # Patrón SINGLETON: Garantiza que solo exista una única vista/creador en todo el juego
    def __new__(cls):
        if cls._instancia is None:
            # Si no existe, la creamos
            cls._instancia = super(VistaLaberinto_Clase, cls).__new__(cls)
            cls._instancia.juego = None
            cls._instancia._configurar_emojis()
        # Si ya existe, devolvemos la misma de siempre
        return cls._instancia

    # Método de inicialización separado de la instancia global
    def _configurar_emojis(self):
        self.t_pared = "🧱"
        self.t_puerta_cerrada = "🚪"
        self.t_puerta_abierta = "🕳️ " # Pasaje oscuro abierto
        self.t_suelo = "⬛"
        self.t_prota = "🤺" # Nuestro héroe Hollow Knight
        self.t_bicho_agresivo = "👹"
        self.t_bicho_perezoso = "😴"
        self.t_armario = "🗄️ "
        self.t_bomba = "💣"
        self.t_generico = "📦"

    def crear_juego_desde_json(self, ruta_json):
        """ Fachada: La vista se encarga de crear el juego completo usando el Builder y Director """
        with open(ruta_json, "r", encoding="utf-8") as fichero:
            diccionario = json.load(fichero)
            
        builder = LaberintoBuilder_Clase()
        director = Director_Clase()
        self.juego = director.procesar(diccionario, builder)
        return self.juego

    def dibujar_habitacion(self, habitacion):
        if not self.juego:
            print("Error: No puedes renderizar antes de llamar a crear_juego_desde_json()")
            return
            
        print(f"\n🔮 --- VISTA DE SATÉLITE: HABITACIÓN {habitacion.num} --- 🔮")
        # Cuadrícula 5x5
        grid = [[self.t_suelo for _ in range(5)] for _ in range(5)]
        
        # --- 1. CONSTRUIMOS LOS MUROS EXTERIORES ---
        for i in range(5):
            grid[0][i] = self.t_pared # Muro Norte
            grid[4][i] = self.t_pared # Muro Sur
            grid[i][0] = self.t_pared # Muro Oeste
            grid[i][4] = self.t_pared # Muro Este

        # --- 2. INSTALAMOS LAS PUERTAS ---
        def pintar_orilla(elemento, y, x):
            if elemento is not None:
                if getattr(elemento, 'EsPuerta', lambda: False)():
                    if getattr(elemento, 'estaAbierta', lambda: False)():
                        grid[y][x] = self.t_puerta_abierta
                    else:
                        grid[y][x] = self.t_puerta_cerrada
                else:
                    grid[y][x] = self.t_pared 

        pintar_orilla(habitacion.obtener_elemento(Norte()), 0, 2)
        pintar_orilla(habitacion.obtener_elemento(Sur()), 4, 2)
        pintar_orilla(habitacion.obtener_elemento(Este()), 2, 4)
        pintar_orilla(habitacion.obtener_elemento(Oeste()), 2, 0)

        # --- 3. AMUEBLAMOS CON LOS HIJOS (Armarios, Bombas, etc) ---
        pos_esquinas = [(1,1), (1,3), (3,1), (3,3)]
        for hijo in habitacion.hijos:
            if not pos_esquinas:
                break 
            y, x = pos_esquinas.pop(0)
            tipo_hijo = type(hijo).__name__.lower()
            if "armario" in tipo_hijo:
                grid[y][x] = self.t_armario
            elif "bomba" in tipo_hijo or getattr(hijo, 'EsBomba', lambda: False)():
                grid[y][x] = self.t_bomba
            else:
                grid[y][x] = self.t_generico
                
        # --- 4. TRAEMOS A LOS SERES VIVOS ---
        if self.juego.personaje is not None and getattr(self.juego.personaje, 'posicion', None) == habitacion:
            grid[2][2] = self.t_prota
            
        pos_bichos = [(1,2), (3,2), (2,1), (2,3)]
        for bicho in self.juego.bichos:
            if getattr(bicho, 'posicion', None) == habitacion and bicho.estaVivo():
                if pos_bichos:
                    by, bx = pos_bichos.pop(0)
                else:
                    by, bx = 2, 2 
                
                if getattr(bicho, 'esAgresivo', lambda: False)():
                    grid[by][bx] = self.t_bicho_agresivo
                elif getattr(bicho, 'esPerezoso', lambda: False)():
                    grid[by][bx] = self.t_bicho_perezoso
                else:
                    grid[by][bx] = "👾" 

        # --- 5. RENDERIZAMOS Y PINTAMOS EN CONSOLA ---
        for fila in grid:
            print("  ".join(fila))
            
        print("="*38 + "\n")

# =========================================================================
# BLOQUE DE EJECUCIÓN DIRECTA (VISUALIZADOR RÁPIDO)
# =========================================================================
if __name__ == "__main__":
    print("="*50)
    print("   👁️  TESTER RÁPIDO DE JSONS (VISTA LABERINTO)")
    print("="*50)
    
    # Cambia esta ruta por el JSON que quieras explorar rápidamente
    ruta_json_prueba = r"C:\Uni\3º ESIIAB\2º cuatri\Diseño\Prácticas\1ºEntrega\Archivos Json\Laberinto26-4Habs-bichos.json"
    
    try:
        print(f"> Abriendo plano: {ruta_json_prueba}...\n")
        vista = VistaLaberinto_Clase()
        juego_generado = vista.crear_juego_desde_json(ruta_json_prueba)
        
        # Iteramos y dibujamos automáticamente todas las habitaciones del JSON
        # Asumiendo que las habitaciones están conectadas como 'hijos' del laberinto
        for habitacion_creada in juego_generado.laberinto.hijos:
            vista.dibujar_habitacion(habitacion_creada)
            
    except FileNotFoundError:
        print(f"❌ Error: No se ha encontrado el archivo '{ruta_json_prueba}'.")
        print("Asegúrate de que la ruta es correcta.")
