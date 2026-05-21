import math
import random
import time
from Laberinto26.Comandos.Comando import Comando_Clase

class InteractuarComando(Comando_Clase):
    def __init__(self, interfaz):
        super().__init__(interfaz)

    def ejecutar(self, alguien=None):
        from Laberinto26.MainInterfaz import FloatingText, Particle
        interfaz = self.receptor
        armarios = [h for h in interfaz.hab_actual.hijos if h.__class__.__name__ in ('Armario_Clase', 'ArmarioBombaVeneno')] if interfaz.hab_actual else []
        cercano = None
        for arm in armarios:
            dist = math.hypot(interfaz.player.x - arm.x, interfaz.player.y - arm.y)
            if dist <= 50:
                cercano = arm
                break
        
        if cercano:
            if cercano.__class__.__name__ == 'ArmarioBombaVeneno':
                if getattr(cercano, 'abierto', False):
                    interfaz.floating_texts.append(FloatingText(
                        cercano.x, cercano.y - 40, "El armario está destruido 🚪", "#aaaaaa", ("Consolas", 11, "bold")
                    ))
                else:
                    cercano.abierto = True
                    cercano.activa = False
                    
                    interfaz.player_poison_ticks = 10
                    interfaz.player_poison_last_tick = time.time()
                    
                    interfaz.screen_shake = 22
                    
                    interfaz.floating_texts.append(FloatingText(
                        cercano.x, cercano.y - 45, "💥 ¡TRAMPA EXPLOSIVA! 🧪☠️", "#20df40", ("Consolas", 13, "bold")
                    ))
                    
                    print("💥 ¡BOOM! El armario bomba de veneno ha explotado, envenenando a Hollow Knight.")
                    
                    for _ in range(40):
                        interfaz.particles.append(Particle(
                            cercano.x, cercano.y, random.uniform(-6, 6), random.uniform(-6, 6),
                            random.choice(["#20df40", "#32cd32", "#00ff00", "#105010"]),
                            random.randint(3, 7), 35
                        ))
            else:
                if getattr(cercano, 'abierto', False):
                    interfaz.floating_texts.append(FloatingText(
                        cercano.x, cercano.y - 40, "El armario está vacío 🚪", "#aaaaaa", ("Consolas", 11, "bold")
                    ))
                else:
                    cercano.abierto = True
                    # 🎁 Mejoramos drásticamente el botín (Loot Buff): garantizamos llave + altas probabilidades de objetos de alta calidad
                    dropped = ["llave"]
                    if random.random() < 0.75:
                        dropped.append("espada")
                    if random.random() < 0.80:
                        dropped.append("pocion")
                    if random.random() < 0.70:
                        dropped.append("armadura")
                        
                    if dropped:
                        if interfaz.hab_actual.num not in interfaz.room_floor_items:
                            interfaz.room_floor_items[interfaz.hab_actual.num] = []
                        for idx, item_tipo in enumerate(dropped):
                            offset_x = random.randint(-40, 40)
                            offset_y = 35 + idx * 10
                            interfaz.room_floor_items[interfaz.hab_actual.num].append({
                                "x": cercano.x + offset_x,
                                "y": cercano.y + offset_y,
                                "tipo": item_tipo
                            })
                        interfaz.floating_texts.append(FloatingText(
                            cercano.x, cercano.y - 45, "¡Armario abierto! 🎁", "#ffd700", ("Consolas", 12, "bold")
                        ))
                    else:
                        interfaz.floating_texts.append(FloatingText(
                            cercano.x, cercano.y - 45, "¡Vaya, estaba vacío! 💨", "#aaaaaa", ("Consolas", 11, "bold")
                        ))
                    
                    for _ in range(25):
                        interfaz.particles.append(Particle(
                            cercano.x, cercano.y, random.uniform(-4, 4), random.uniform(-4, 4),
                            "#6a0dad", random.randint(2, 4), 30
                        ))
