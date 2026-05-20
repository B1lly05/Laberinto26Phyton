from Laberinto26.ElementosFisicos.ElementoMapa import ElementoMapa_Clase

class Hoja_Clase(ElementoMapa_Clase):
  def __init__(self):
    super().__init__()

  def aceptar(self, visitor):
    super().aceptar(visitor)
