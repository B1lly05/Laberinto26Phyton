from Laberinto26.ElementosFisicos.Hoja import Hoja_Clase
from Laberinto26.Estados.Cerrada import Cerrada

class Puerta_Clase(Hoja_Clase):
  def __init__(self,nombre = "Puerta sin nombre"):
    super().__init__()
    self.estado = Cerrada() 
    self.lado1 = None
    self.lado2 = None
    self.nombre = nombre
    
  def EsPuerta(self):
    return True
    
  def abrir_puerta(self):
    print(f"Abrimos la puerta {self}")
    self.estado.abrir(self)

  def cerrar_puerta(self):
    print(f"Cerramos la puerta {self}")
    self.estado.cerrar(self)

  def __str__(self): 
    return self.nombre 
  
  def estaAbierta(self):
    return self.estado.estaAbierta()

  def entrar(self, alguien):
        self.estado.entrar(alguien, self)

  def aceptar(self, visitor):
        visitor.visitar_puerta(self)
