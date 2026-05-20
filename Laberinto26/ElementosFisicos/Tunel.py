from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class Tunel(Hoja_Clase):
    def __init__(self, juego=None):
        super().__init__()
        self.laberinto = None
        self.juego = juego

    def EsTunel(self):
        return True

    def entrar(self, alguien):
        if self.laberinto is None:
            print("...[Proxy] Tunel clonando laberinto perezosamente...")
            if self.juego:
                # Simulación de clonar el laberinto, para evitar clonado profundo complejo, 
                # llamamos a fabricar de nuevo o usamos el mismo para la prueba.
                self.laberinto = self.juego.crear_laberinto_2_habitacionesFM()
            else:
                raise ValueError("El tunel necesita conocer el juego para clonar el laberinto.")
        
        print(f"{alguien} ha entrado al Túnel y ha sido transportado a un nuevo laberinto clonado.")
        self.laberinto.entrar_contenedor(alguien)
