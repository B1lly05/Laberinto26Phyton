import random
from Laberinto26.Comandos.Comando import Comando_Clase

class UsarPocionComando(Comando_Clase):
    def __init__(self, interfaz):
        super().__init__(interfaz)

    def ejecutar(self, alguien=None):
        from Laberinto26.MainInterfaz import FloatingText, Particle
        interfaz = self.receptor
        if interfaz.inventario["pocion_salud"] > 0:
            interfaz.inventario["pocion_salud"] -= 1
            max_health = 50 + interfaz.inventario["armadura"] * 25
            interfaz.prota.vidas = max_health
            interfaz.floating_texts.append(FloatingText(
                interfaz.player.x, interfaz.player.y - 45, "Salud al 100% 🧪❤️", "#00ff00", ("Consolas", 14, "bold")
            ))
            for _ in range(25):
                interfaz.particles.append(Particle(
                    interfaz.player.x, interfaz.player.y, random.uniform(-3, 3), random.uniform(-3, 3),
                    "#00ff00", random.randint(2, 4), 30
                ))
        else:
            interfaz.floating_texts.append(FloatingText(
                interfaz.player.x, interfaz.player.y - 30, "¡Sin pociones! 🔒", "#ff3333", ("Consolas", 12, "bold")
            ))
