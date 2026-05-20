import sys
import os
# Añadir la raíz del proyecto al path para que funcionen los imports de paquete
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from Laberinto26_builder.VistaLaberinto import VistaLaberinto_Clase
from Laberinto26.Entidades.Bicho import Bicho_Clase
from Laberinto26.Entidades.Perezoso import Perezoso
from Laberinto26.Orientaciones.Sur import Sur

print("="*60)
print("             MEGAMAIN - LABERINTO PATRONES (BUILDER)")
print("="*60)

# El Renderizador/Ensamblador ahora es único en toda la partida (PATRÓN SINGLETON)
vista = VistaLaberinto_Clase()

# 1. INICIALIZAMOS EL JUEGO Y EL LABERINTO DESDE LA VISTA ÚNICA
print("\n[1] CREANDO EL MUNDO A TRAVÉS DE LA VISTA (JSON)...")
ruta = r"C:\Uni\3º ESIIAB\2º cuatri\Diseño\Prácticas\1ºEntrega\Archivos Json\Laberinto26-4Habs-bichos.json"
mi_juego = vista.crear_juego_desde_json(ruta)
mi_laberinto = mi_juego.laberinto

print("\n================ RENDER INICIAL ======================")
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(1))
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(2))

# 2. COLOCAMOS AL PROTAGONISTA Y EXTRAS MANUALES
print("\n[2] INTRODUCIENDO AL PROTAGONISTA...")
mi_juego.agregar_personaje("Hollow Knight")

print("\n[3] INVOCANDO Y ACOMODANDO A LOS EXTRAS...")
# Opcional: invocar orcos manuales extra que no estaban en el JSON
orco = Bicho_Clase(Perezoso(), "Orco Shrek Manual")
mi_juego.agregar_bicho(orco)
mi_laberinto.obtener_habitacion(2).entrar(orco)

# 4. PATRÓN ITERATOR AL RESCATE
print("\n[4] EL DIOS DEL LABERINTO ABRE LAS PUERTAS (ITERATOR)")
mi_juego.abrir_todas_las_puertas()

print("\n================ RENDER CON PUERTAS ABIERTAS ======================")
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(1))
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(2))

# 5. LANZAMOS LA IA / MOVIMIENTO
print("\n[5] LANZANDO EL MOVIMIENTO DE IA Y PROTA...")
print("> Trato de que Hollow Knight camine hacia el Sur desde la Habitación 1...")
if getattr(mi_laberinto.obtener_habitacion(1).obtener_elemento(Sur()), 'EsPuerta', lambda: False)():
    print("¡Efectivamente, en el sur de la Hab 1 hay una puerta!")
    mi_laberinto.obtener_habitacion(1).obtener_elemento(Sur()).entrar(mi_juego.personaje)

print("\n================ RENDER FINAL ======================")
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(1))
vista.dibujar_habitacion(mi_laberinto.obtener_habitacion(2))

# 6. EXTERMINIO Y FIN DEL JUEGO
print("\n[6] FIN DE LA PARTIDA: EXTERMINANDO BICHOS Y APAGANDO")
mi_juego.terminar_todos_los_bichos()

print("\n================= FIN DEL JUEGO ====================")
