from Laberinto26.Estados.EstadoPuerta import EstadoPuerta_Clase

class Cerrada(EstadoPuerta_Clase):
    def abrir(self, puerta):
        from Laberinto26.Estados.Abierta import Abierta
        puerta.estado = Abierta()

    def cerrar(self, puerta):
        print(f"La {puerta.nombre} ya estaba cerrada.")

    def entrar(self, alguien, puerta):
        print(f"La {puerta.nombre} está cerrada. ¡PUM! ({alguien} se ha chocado)")

    def estaAbierta(self):
        return False
