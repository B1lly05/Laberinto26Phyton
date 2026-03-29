import time
from Juego import Juego_Clase
from Prota import Prota_Clase
from Bicho import Bicho_Clase
from Modo import Agresivo, Perezoso

print("="*60)
print("             MEGAMAIN - LABERINTO PATRONES")
print("="*60)

# 1. INICIALIZAMOS EL JUEGO Y EL LABERINTO MÁS COMPLETO
print("\n[1] CREANDO EL MUNDO...")
juego = Juego_Clase()
juego.crear_laberinto_4_habitacionesFMBOMBAS()
print("Laberinto de 4 habitaciones y 2 bombas (hab 1 y 3) fabricado correctamente.")

# 2. COLOCAMOS AL PROTAGONISTA
print("\n[2] INTRODUCIENDO AL PROTAGONISTA...")
print("(Al entrar a la hab 1, debería comerse una bomba inactiva por defecto o activa si lo está)")
juego.agregar_personaje("Arturo")

juego.activar_todas_las_bombas()
# 3. CREAMOS LOS MONSTRUOS Y LOS PONEMOS EN HABITACIONES
print("\n[3] INVOCANDO A LOS BICHOS...")
# Bicho agresivo en la habitación 2 (se mueve rápido)
dragon = Bicho_Clase(Agresivo(), "Dragón Balerion")
juego.agregar_bicho(dragon)
juego.obtener_habitacion(2).entrar(dragon)

# Bicho perezoso en la habitación 3 (tiene una BOMBA, ¡veremos si le explota al entrar!)
orco = Bicho_Clase(Perezoso(), "Orco Shrek")
juego.agregar_bicho(orco)
juego.obtener_habitacion(3).entrar(orco)

# 4. LANZAMOS LA CONCURRENCIA (HILOS)
print("\n[4] LANZANDO LA IA DE TERROR...")
juego.lanzar_todos_los_bichos()

# Dejamos que los bichos se den cabezazos contra las puertas cerradas un par de segundos
print("\n--- Esperando 3 segundos de caos con las puertas cerradas... ---")
time.sleep(3)

# 5. PATRÓN ITERATOR AL RESCATE
print("\n[5] EL DIOS DEL LABERINTO ABRE LAS PUERTAS (ITERATOR)")
juego.abrir_todas_las_puertas()

print("\n--- Esperando 5 segundos para que los bichos caminen entre habitaciones... ---")
time.sleep(5)

# 6. EXTERMINIO Y FIN DEL JUEGO
print("\n[6] FIN DE LA PARTIDA: EXTERMINANDO BICHOS Y APAGANDO")
juego.terminar_todos_los_bichos()

print("\n================= FIN DEL JUEGO ====================")
