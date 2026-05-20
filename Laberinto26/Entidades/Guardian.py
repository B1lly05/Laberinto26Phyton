import time
from Laberinto26.Entidades.Modo import Modo_Clase

class Guardian(Modo_Clase):
    """Modo de comportamiento del Guardián del Laberinto (Boss Final).
    
    Es agresivo por naturaleza, con un ciclo de sueño extremadamente corto (0.5 seg)
    ya que está siempre alerta protegiendo la salida del laberinto.
    """

    def duerme(self, un_bicho):
        print(f"{un_bicho} vigila sin descanso (0.5 segundos)")
        time.sleep(0.5)

    def esAgresivo(self):
        return True

    def esGuardian(self):
        return True

    def __str__(self):
        return "Guardian"
