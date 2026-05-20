from Laberinto26.Estados.EstadoPuerta import EstadoPuerta_Clase

class Abierta(EstadoPuerta_Clase):
    def abrir(self, puerta):
        print(f"La {puerta.nombre} ya estaba abierta.")

    def cerrar(self, puerta):
        from Laberinto26.Estados.Cerrada import Cerrada
        puerta.estado = Cerrada()

    def entrar(self, alguien, puerta):
        if alguien.posicion == puerta.lado1:
            puerta.lado2.entrar_habitacion(alguien)
        else:
            puerta.lado1.entrar_habitacion(alguien)

    def estaAbierta(self):
        return True
