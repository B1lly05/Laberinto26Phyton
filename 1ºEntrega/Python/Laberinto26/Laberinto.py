from .Contenedor import Contenedor_Clase

class Laberinto_Clase(Contenedor_Clase):
    def __init__(self):
        super().__init__()

    def entrar_laberinto(self, alguien):
        print(f"{alguien} ha osado entraral laberinto")
        self.obtener_habitacion(1).entrar(alguien)

    def recorrer(self, UnBloque):
        print('Recorriendo el laberinto')
        for hijo in self.hijos:
            hijo.recorrer(UnBloque)

    def obtener_habitacion(self, numero):
        for hijo in self.hijos:
            if hasattr(hijo, 'num') and hijo.num == numero:
                return hijo
        return None  # Si no la encuentra

