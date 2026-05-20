from Laberinto26.Juego import Juego_Clase
from Laberinto26.ElementosFisicos.ParedBomba import ParedBomba

class JuegoBombas(Juego_Clase):
    def __init__(self):
        super().__init__()

    # FACTORY METHOD: Sobrescribimos la creación de paredes
    def fabricar_pared(self):
        return ParedBomba()
