from Laberinto26.ElementosFisicos.Pared import Pared_Clase

class ParedBomba(Pared_Clase):
    def __init__(self):
        super().__init__()
        self.activa = True

    def entrar(self, alguien):
        if self.activa:
            print(f"¡BOOOM! {alguien} se ha chocado con una PARED BOMBA y ha explotado.")
            if hasattr(alguien, 'vidas'):
                alguien.vidas = 0
            self.activa = False # Ya explotó
        else:
            print(f"{alguien} se ha chocado con los restos humeantes de una pared bomba.")

    def __str__(self): 
        return "ParedBomba"
