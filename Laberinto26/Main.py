import sys
import os
import io

# Add the parent directory to sys.path so we can import Laberinto26
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure console to support emojis in Windows safely
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from Laberinto26_builder.VistaLaberinto import VistaLaberinto_Clase
from Laberinto26.Entidades.Prota import Prota_Clase
from Laberinto26.Orientaciones.Norte import Norte
from Laberinto26.Orientaciones.Sur import Sur
from Laberinto26.Orientaciones.Este import Este
from Laberinto26.Orientaciones.Oeste import Oeste
from Laberinto26.Comandos.Abrir import Abrir

def mostrar_mapa_completo(prota_posicion):
    coordenadas = {
        14: (5, 4),
        13: (4, 4),
        12: (3, 4),
        10: (3, 0),
        11: (3, 1),
        9:  (2, 1),
        6:  (2, 3),
        7:  (2, 4),
        8:  (2, 5),
        2:  (1, 0),
        3:  (1, 1),
        4:  (1, 2),
        5:  (1, 3),
        1:  (0, 1),
        15: (0, 3),
        16: (0, 4),
        18: (0, 5)
    }
    
    print("\n🗺️  --- MAPA COMPLETO DEL LABERINTO --- 🗺️")
    print("Leyenda: [Hxx] = Habitación | [ 🤺 ] = Tu Posición actual\n")
    
    for r in range(5, -1, -1):
        linea_habs = ""
        for c in range(6):
            encontrado = None
            for num, coord in coordenadas.items():
                if coord == (r, c):
                    encontrado = num
                    break
            
            if encontrado is not None:
                if prota_posicion and prota_posicion.num == encontrado:
                    linea_habs += "[ 🤺 ]"
                else:
                    linea_habs += f"[H{encontrado:02d}]"
            else:
                linea_habs += "      "
        print(linea_habs)
    print("="*40 + "\n")

def main():
    print("="*60)
    print(" 🎮  LABERINTO26: COMPROBACIÓN DE LÓGICA DE HABITACIONES, PUERTAS Y BOMBAS  🎮")
    print("="*60)
    
    ruta_oficial = r"C:\Uni\3º ESIIAB\2º cuatri\Diseño\Prácticas\1ºEntrega\Python\Mapa\Laberinto Del Olimpo.json"
    ruta_local_fallback = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Mapa', 'Laberinto Del Olimpo.json'))
    
    vista = VistaLaberinto_Clase()
    juego = None
    
    try:
        print(f"[🔍] Buscando JSON del Olimpo en ruta oficial: {ruta_oficial}...")
        juego = vista.crear_juego_desde_json(ruta_oficial)
        print("✅ JSON oficial del Olimpo cargado con éxito.")
    except FileNotFoundError:
        print(f"⚠️  Ruta oficial no encontrada. Cargando copia de seguridad local: {ruta_local_fallback}...")
        try:
            juego = vista.crear_juego_desde_json(ruta_local_fallback)
            print("✅ Copia local del Olimpo cargada con éxito.")
        except FileNotFoundError:
            print("❌ Error crítico: No se ha podido encontrar el archivo JSON del Olimpo en ninguna ubicación.")
            return




    vista.juego = juego
    
    juego.agregar_personaje("Hollow Knight")
    prota = juego.personaje
    
    direcciones_validas = {
        'n': Norte(),
        's': Sur(),
        'e': Este(),
        'o': Oeste()
    }
    
    # 🛡️ Buff de inicio: Hollow Knight comienza con 100 de salud máxima y equipamiento básico
    prota.vidas = 100
    inventario = {"llave": 1, "espada_olimpo": 1, "pocion_salud": 1, "armadura": 1}
    player_poison_ticks = 0
    anterior_habitacion = None
    
    print(f"\n✨ ¡{prota.nombre} ha entrado en el Laberinto! Comienza en la {prota.posicion}. ✨")
    print("El objetivo es sobrevivir, combatir enemigos, abrir armarios y escapar con vida.\n")
    
    # Bucle principal interactivo
    while prota.estaVivo():
        # 1. Al entrar en la habitación, detectamos trampas (bombas) ocultas
        hijos_bombas = [h for h in prota.posicion.hijos if getattr(h, 'EsBomba', lambda: False)() and getattr(h, 'activa', True)]
        if hijos_bombas:
            print(f"\n👁️  [PERCEPCIÓN] Notas que el suelo tiene {len(hijos_bombas)} baldosas sospechosamente agrietadas...")
            print("  -> Puedes intentar avanzar con cuidado o usar la acción 'desarmar' para neutralizarlas de forma segura.")
            
            import random
            for bomba in hijos_bombas:
                # 75% de probabilidad de esquivarlas de manera pasiva gracias a la agilidad del prota
                if random.random() < 0.25:
                    bomba.activa = False
                    is_ven = getattr(bomba, 'EsBombaVeneno', lambda: False)()
                    if is_ven:
                        print("🧪🤢 ¡ZAS! Tropiezas con una baldosa rota de Veneno. ¡Sufres 2 de daño y te envenenas!")
                        prota.vidas = max(0, prota.vidas - 2)
                        player_poison_ticks = 10
                    else:
                        print("💥💥 ¡BOOM! Tropiezas con una trampa de presión. Sufres 3 de daño.")
                        prota.vidas = max(0, prota.vidas - 3)
                else:
                    print("💨 Pasas con cuidado y esquivas una baldosa agrietada sospechosa sin activarla.")
                    
                if not prota.estaVivo():
                    break

        if not prota.estaVivo():
            print(f"\n💀💀💀 {prota.nombre} ha muerto a causa de las trampas del laberinto. 💀💀💀")
            break

        # 2. Procesar recolección automática de Loot tirado en el suelo
        hijos_loot = [h for h in list(prota.posicion.hijos) if h.__class__.__name__ in ('Llave', 'PocionSalud', 'EspadaOlimpo', 'Armadura_Clase')]
        for loot in hijos_loot:
            tipo = loot.__class__.__name__
            if tipo == 'Llave':
                inventario["llave"] += 1
                print("🔑 ¡Has encontrado una Llave tirada en el suelo!")
            elif tipo == 'PocionSalud':
                inventario["pocion_salud"] += 1
                print("🧪 ¡Has encontrado una Poción de Salud en el suelo!")
            elif tipo == 'EspadaOlimpo':
                inventario["espada_olimpo"] = max(1, inventario["espada_olimpo"] + 1)
                print(f"⚔️ ¡Has encontrado la Espada del Olimpo! Nivel: {inventario['espada_olimpo']}")
            elif tipo == 'Armadura_Clase':
                inventario["armadura"] = max(1, inventario["armadura"] + 1)
                print(f"🛡️ ¡Has encontrado una Armadura! Nivel: {inventario['armadura']}")
            prota.posicion.hijos.remove(loot)

        # 3. Comprobación y fase de combate con enemigos vivos en esta habitación
        bichos_combate = [b for b in juego.bichos if getattr(b, 'posicion', None) == prota.posicion and b.estaVivo()]
        if bichos_combate:
            print("\n" + "⚔️" * 15 + " ¡FASE DE COMBATE! " + "⚔️" * 15)
            print(f"¡Te has topado con {len(bichos_combate)} enemigos hostiles en la sala!")
            
            while bichos_combate and prota.estaVivo():
                # Actualizar lista de enemigos por si murieron
                bichos_combate = [b for b in bichos_combate if b.estaVivo()]
                if not bichos_combate:
                    break
                
                print(f"\n❤️ {prota.nombre}: {prota.vidas} HP | ⚔️ Espada Nvl: {inventario['espada_olimpo']} | 🛡️ Armadura Nvl: {inventario['armadura']} | 🧪 Pociones: {inventario['pocion_salud']}")
                print("Enemigos en la sala:")
                for idx, b in enumerate(bichos_combate):
                    print(f"  [{idx}] {b.nombre} - Vida: {b.vidas} HP | Poder: {b.poder}")
                
                print("\nOpciones de combate:")
                print("  - [A] Atacar a un enemigo")
                print("  - [H] / [U] Curarte con una Poción (restaura salud al 100%)")
                print("  - [E] Huir de la sala (regresar a la habitación anterior)")
                
                cmd_combate = input("Elige acción de combate: ").strip().lower()
                if cmd_combate == 'a':
                    if len(bichos_combate) > 1:
                        try:
                            target = int(input("Elige el índice del enemigo a atacar: ").strip())
                            if target < 0 or target >= len(bichos_combate):
                                print("❌ Índice inválido.")
                                continue
                        except ValueError:
                            print("❌ Debes introducir un número.")
                            continue
                    else:
                        target = 0
                        
                    enemigo = bichos_combate[target]
                    # Calcular daño (Buff: nivel 0 hace 15, nivel 1 hace 25, nivel 2 hace 32, escala +7 por nivel)
                    lvl = inventario["espada_olimpo"]
                    dmg = 15 if lvl == 0 else (18 + lvl * 7)
                    enemigo.vidas = max(0, enemigo.vidas - dmg)
                    print(f"💥 ¡Golpeas a {enemigo.nombre} infligiendo {dmg} de daño!")
                    
                    if not enemigo.estaVivo():
                        print(f"💀 ¡{enemigo.nombre} ha sido derrotado!")
                        
                        # Probabilidades de drops por parte de los monstruos
                        is_agresivo = getattr(enemigo, 'esAgresivo', lambda: False)()
                        is_guardian = getattr(enemigo, 'esGuardian', lambda: False)()
                        
                        if is_agresivo:
                            import random
                            if random.random() < 0.30:
                                from Laberinto26.ElementosFisicos.PocionSalud import PocionSalud
                                prota.posicion.agregar_hijo(PocionSalud())
                                print("🧪 ¡El enemigo ha dropeado una Poción de Salud en el suelo!")
                            if random.random() < 0.30:
                                from Laberinto26.ElementosFisicos.Llave import Llave
                                prota.posicion.agregar_hijo(Llave())
                                print("🔑 ¡El enemigo ha dropeado una Llave en el suelo!")
                                
                        if is_guardian:
                            from Laberinto26.ElementosFisicos.EspadaOlimpo import EspadaOlimpo
                            from Laberinto26.ElementosFisicos.PocionSalud import PocionSalud
                            prota.posicion.agregar_hijo(EspadaOlimpo())
                            prota.posicion.agregar_hijo(PocionSalud())
                            print("⚔️ ¡El Guardián ha dropeado la Espada del Olimpo y una Poción de Salud en el suelo!")

                        if enemigo in juego.bichos:
                            juego.bichos.remove(enemigo)
                            
                elif cmd_combate in ('h', 'u'):
                    if inventario["pocion_salud"] > 0:
                        inventario["pocion_salud"] -= 1
                        max_health = 100 + inventario["armadura"] * 25
                        prota.vidas = max_health
                        print(f"🧪❤️ ¡Usas una poción! Vuelves a tener {max_health} HP.")
                    else:
                        print("❌ No tienes pociones de salud.")
                        continue
                        
                elif cmd_combate == 'e':
                    if anterior_habitacion:
                        print("🏃‍♂️ ¡Huyes despavorido de regreso!")
                        prota.posicion = anterior_habitacion
                        break
                    else:
                        print("❌ No puedes huir, ¡esta es la entrada del laberinto!")
                        continue
                else:
                    print("❌ Acción no válida.")
                    continue
                
                # Turno de los bichos supervivientes (¡el jugador siempre ataca antes!)
                bichos_combate = [b for b in bichos_combate if b.estaVivo()]
                if bichos_combate and prota.estaVivo() and cmd_combate != 'u':
                    print("\n👊 ¡Los enemigos intentan contraatacar!")
                    import random
                    for b in bichos_combate:
                        # 1. Bicho Perezoso: 50% de probabilidad de dormirse y fallar
                        if getattr(b, 'esPerezoso', lambda: False)() and random.random() < 0.50:
                            print(f"  - 💤 ¡{b.nombre} se queda profundamente dormido a mitad de combate y falla su golpe!")
                            continue
                        
                        # 2. Bicho Agresivo: 20% de probabilidad de fallar por rabia/precipitación
                        elif getattr(b, 'esAgresivo', lambda: False)() and random.random() < 0.20:
                            print(f"  - 💢 ¡{b.nombre} ataca con tanta furia descontrolada que falla el golpe por completo!")
                            continue
                            
                        # 3. Guardián del Laberinto (Boss): 10% de probabilidad de fallar su ataque pesado
                        elif getattr(b, 'esGuardian', lambda: False)() and random.random() < 0.10:
                            print(f"  - 🛡️ ¡{b.nombre} golpea el suelo con su gran maza agrietando las baldosas pero fallándote!")
                            continue
                        
                        # Ataque acertado
                        dmg_bicho = b.poder
                        # Aplicar reducción de armadura (Buff: +2 base, +4 por nivel)
                        arm_reduction = inventario["armadura"] * 4 + 2
                        dmg_final = max(1, dmg_bicho - arm_reduction)
                        prota.vidas = max(0, prota.vidas - dmg_final)
                        print(f"  - 💥 ¡{b.nombre} te golpea y te hace {dmg_final} de daño! (Reducido {arm_reduction} por armadura).")
            
            print("=" * 60)
            if not prota.estaVivo():
                print(f"\n💀💀💀 {prota.nombre} ha perecido en combate. 💀💀💀")
                break
            if cmd_combate == 'u':
                # Si huimos, saltamos al inicio del bucle en la habitación anterior
                continue

        # Renderizamos la habitación actual utilizando la vista
        vista.dibujar_habitacion(prota.posicion)
        
        # Estado actual del héroe
        estado_veneno = f" | 🧪 Veneno activo ({player_poison_ticks} turnos)" if player_poison_ticks > 0 else ""
        print(f"❤️  ESTADO DE {prota.nombre.upper()}: Vidas: {prota.vidas} | Estado: {type(prota.estado).__name__}{estado_veneno}")
        print(f"🎒 INVENTARIO: Llaves: {inventario['llave']} | Pociones: {inventario['pocion_salud']} | Espada Nvl: {inventario['espada_olimpo']} | Armadura Nvl: {inventario['armadura']}")
        
        # Describir la salidas
        print(f"\n📍 Salidas de la {prota.posicion}:")
        for dir_name, dir_obj in direcciones_validas.items():
            elemento = prota.posicion.obtener_elemento(dir_obj)
            tipo_elem = type(elemento).__name__ if elemento else "Vacío"
            if elemento and hasattr(elemento, 'estaAbierta'):
                estado_pt = "Abierta" if elemento.estaAbierta() else "Cerrada"
                tipo_elem = f"Puerta ({estado_pt})"
            print(f"  - [{dir_name.upper()}]: {tipo_elem}")
            
        print("\n🎮 CONTROLES:")
        print("  - Moverse: Escribe 'N', 'S', 'E', o 'O'")
        print("  - Command Pattern: 'abrir [dirección]' (ej. 'abrir s' abre la puerta en esa dirección con llave)")
        print("  - Interactuar: 'I' o 'interactuar' (abre armarios y cofres de la sala)")
        print("  - Desarmar trampas: 'desarmar' o 'D' (desactiva de forma segura todas las bombas del suelo)")
        print("  - Curarse: 'U' o 'H' o 'curar' (usa una poción de salud)")
        print("  - Ver Mapa: Escribe 'M'")
        print("  - Visitor Pattern:")
        print("      * 'A' - Abrir todas las puertas del laberinto")
        print("      * 'C' - Cerrar todas las puertas del laberinto")
        print("      * 'X' - Activar todas las bombas del laberinto")
        print("      * 'Z' - Desactivar todas las bombas del laberinto")
        print("  - 'Q' - Terminar prueba")
        print("-" * 60)
        
        accion = input("Introduce acción: ").strip().lower()
        print("-" * 60)
        
        if accion == 'q':
            print("👋 Finalizando la prueba del laberinto.")
            break
            
        elif accion in ('u', 'h', 'curar'):
            if inventario["pocion_salud"] > 0:
                inventario["pocion_salud"] -= 1
                max_health = 100 + inventario["armadura"] * 25
                prota.vidas = max_health
                print(f"\n🧪❤️ ¡Usas una poción! Vuelves a tener {max_health} HP.")
            else:
                print("\n❌ No tienes pociones de salud.")
            
        elif accion == 'm':
            mostrar_mapa_completo(prota.posicion)
            
        elif accion == 'a':
            print("\n🌌 [VISITOR] Abriendo TODAS las puertas del laberinto...")
            juego.abrir_todas_las_puertas()
            
        elif accion == 'c':
            print("\n🌌 [VISITOR] Cerrando TODAS las puertas del laberinto...")
            juego.cerrar_todas_las_puertas()
            
        elif accion == 'x':
            print("\n🌌 [VISITOR] Activando TODAS las bombas del laberinto...")
            juego.activar_todas_las_bombas()
            
        elif accion == 'z':
            print("\n🌌 [VISITOR] Desactivando TODAS las bombas del laberinto...")
            juego.desactivar_todas_las_bombas()
            
        elif accion in ('desarmar', 'd'):
            hijos_bombas = [h for h in prota.posicion.hijos if getattr(h, 'EsBomba', lambda: False)() and getattr(h, 'activa', True)]
            if hijos_bombas:
                print(f"🛠️  {prota.nombre} examina minuciosamente las baldosas agrietadas...")
                for b in hijos_bombas:
                    b.activa = False
                print(f"✅ ¡Has desactivado con éxito {len(hijos_bombas)} baldosas trampa en esta habitación!")
            else:
                print("❌ No hay trampas activas detectadas en el suelo de esta habitación.")
            
        elif accion in ('i', 'interactuar'):
            armarios = [h for h in prota.posicion.hijos if h.__class__.__name__ in ('Armario_Clase', 'ArmarioBombaVeneno')]
            if armarios:
                print("Armarios en la habitación:")
                for idx, arm in enumerate(armarios):
                    estado_arm = "Destruido" if getattr(arm, 'abierto', False) else "Cerrado"
                    print(f"  [{idx}] Armario {arm.num} - Estado: {estado_arm}")
                try:
                    target = int(input("Elige el índice del armario a abrir: ").strip())
                    if target < 0 or target >= len(armarios):
                        print("❌ Índice inválido.")
                        continue
                except ValueError:
                    print("❌ Debes introducir un número.")
                    continue
                
                cercano = armarios[target]
                if getattr(cercano, 'abierto', False):
                    print("🚪 El armario ya está destruido o abierto.")
                else:
                    cercano.abierto = True
                    if cercano.__class__.__name__ == 'ArmarioBombaVeneno':
                        cercano.activa = False
                        print("💥☠️ ¡TRAMPA EXPLOSIVA! El armario de veneno estalla. ¡Sufres 5 de daño y te envenenas!")
                        prota.vidas = max(0, prota.vidas - 5)
                        player_poison_ticks = 10
                    else:
                        print("🚪 Abres el armario de madera...")
                        import random
                        # 🎁 Siempre garantizamos una llave en armarios normales para poder abrir puertas, más otros botines aleatorios
                        dropped = ["llave"]
                        if random.random() < 0.50: dropped.append("espada")
                        if random.random() < 0.50: dropped.append("pocion")
                        if random.random() < 0.50: dropped.append("armadura")
                        
                        if dropped:
                            print("🎁 ¡Encuentras objetos en su interior!")
                            for item in dropped:
                                if item == "llave":
                                    inventario["llave"] += 1
                                    print("  - 🔑 Recoges una Llave.")
                                elif item == "espada":
                                    inventario["espada_olimpo"] = max(1, inventario["espada_olimpo"] + 1)
                                    print(f"  - ⚔️ Recoges la Espada del Olimpo (Nvl {inventario['espada_olimpo']}).")
                                elif item == "pocion":
                                    inventario["pocion_salud"] += 1
                                    print("  - 🧪 Recoges una Poción de Salud.")
                                elif item == "armadura":
                                    inventario["armadura"] = max(1, inventario["armadura"] + 1)
                                    print(f"  - 🛡️ Recoges una Armadura (Nvl {inventario['armadura']}).")
            else:
                print("❌ No hay armarios en esta habitación.")
            
        elif accion.startswith("abrir "):
            partes = accion.split(" ")
            if len(partes) > 1:
                dir_cmd = partes[1]
                if dir_cmd in direcciones_validas:
                    dir_obj = direcciones_validas[dir_cmd]
                    elemento = prota.posicion.obtener_elemento(dir_obj)
                    if elemento and getattr(elemento, 'EsPuerta', lambda: False)():
                        # Si está cerrada, consumimos llave del inventario si tenemos
                        if not elemento.estaAbierta():
                            if inventario["llave"] > 0:
                                inventario["llave"] -= 1
                                cmd = Abrir(elemento)
                                print(f"\n📜 [COMMAND] Usas una llave de tu mochila y abres la puerta al {dir_cmd.upper()}...")
                                cmd.ejecutar()
                            else:
                                print("\n🔒 La puerta está cerrada y no tienes llaves en tu inventario.")
                        else:
                            print("\n🔓 La puerta ya está abierta.")
                    else:
                        print(f"\n❌ No hay una puerta al {dir_cmd.upper()} que se pueda abrir.")
                else:
                    print("\n❌ Dirección no válida. Usa N, S, E, o O.")
            else:
                print("\n❌ Especifica la dirección. Ej: 'abrir s'")
                
        elif accion in direcciones_validas:
            dir_obj = direcciones_validas[accion]
            elemento = prota.posicion.obtener_elemento(dir_obj)
            
            # Si el elemento en esa dirección es una puerta cerrada y tenemos llaves, la abrimos automáticamente
            if elemento and getattr(elemento, 'EsPuerta', lambda: False)() and not elemento.estaAbierta():
                if inventario["llave"] > 0:
                    inventario["llave"] -= 1
                    cmd = Abrir(elemento)
                    print(f"\n📜 [COMMAND] Usas una llave de tu mochila y abres la puerta al {accion.upper()} automáticamente...")
                    cmd.ejecutar()
            
            # Guardar la habitación previa para poder huir
            hab_previa = prota.posicion
            
            print(f"\n👣 Hollow Knight avanza hacia el {accion.upper()}...")
            dir_obj.caminar(prota)
            
            # Si el movimiento fue exitoso
            if prota.posicion != hab_previa:
                anterior_habitacion = hab_previa
                
                # Procesar daño por veneno (Nerf: sólo 2 de daño por turno en lugar de 5)
                if player_poison_ticks > 0:
                    player_poison_ticks -= 1
                    prota.vidas = max(0, prota.vidas - 2)
                    print(f"🧪🤢 ¡El veneno corre por tu sangre! Sufres 2 de daño. (Quedan {player_poison_ticks} turnos de envenenamiento).")
                    
            if not prota.estaVivo():
                print(f"\n💀💀💀 {prota.nombre} ha muerto a causa de las heridas o del veneno. 💀💀💀")
                break
        else:
            print("\n❌ Comando o dirección no reconocidos. Usa N, S, E, O, abrir, interactuar, desarmar, o las opciones del Visitor.")
            
    print("\n================= PRUEBA FINALIZADA ====================")

if __name__ == "__main__":
    main()
