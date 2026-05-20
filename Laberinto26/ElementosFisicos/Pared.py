from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase

class Pared_Clase(Hoja_Clase):
  def __init__(self):
    super().__init__()

  def entrar(self):
    print("Has chocado con una pared")

  def entrar(self,alguien):
    print(f"{alguien} se ha chocado con una pared")
    
  def __str__(self): 
    return getattr(self, "nombre", "Pared")     

  def aceptar(self, visitor):
    visitor.visitar_pared(self)
