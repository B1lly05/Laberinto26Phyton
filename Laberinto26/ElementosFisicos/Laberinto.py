from Laberinto26.ElementosFisicos.Contenedor import Contenedor_Clase

class Laberinto_Clase(Contenedor_Clase):
    def __init__(self):
        super().__init__()

    def entrar_laberinto(self, alguien):
        print(f"{alguien} ha osado entraral laberinto")
        self.obtener_habitacion(1).entrar(alguien)

    def aceptar(self, visitor):
        print('Recorriendo el laberinto con visitor')
        super().aceptar(visitor)

    def obtener_habitacion(self, numero):
        for hijo in self.hijos:
            if hasattr(hijo, 'num') and hijo.num == numero:
                return hijo
        return None  # Si no la encuentra

