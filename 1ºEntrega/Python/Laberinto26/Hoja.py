from .ElementoMapa import ElementoMapa_Clase

class Hoja_Clase(ElementoMapa_Clase):
  def __init__(self):
    super().__init__()

  def  recorrer(self, UnBloque):
    return super().recorrer(UnBloque)



class Pared_Clase(Hoja_Clase):
  def __init__(self):
    super().__init__()

  def entrar(self):
    print("Has chocado con una pared")

  def entrar(self,alguien):
    print(f"{alguien} se ha chocado con una pared")
    
  def __str__(self):  # Con este metodo lo que evitamos es que salga literalmente el valor de la pila del nombre de la puerta y nos ponga el que le pongamos al crear la propia entidad
    return self.nombre     

class Puerta_Clase(Hoja_Clase):
  def __init__(self,nombre = "Puerta sin nombre"):
    super().__init__()
    self.abierta = False 
    self.lado1 = None
    self.lado2 = None
    self.nombre = nombre
    
  def EsPuerta(self):
    return True
    
  def abrir_puerta(self):
    print(f"Abrimos la puerta {self}")
    self.abierta = True

  def cerrar_puerta(self):
    print(f"Cerramos la puerta {self}")
    self.abierta = False

  def __str__(self):  # Con este metodo lo que evitamos es que salga literalmente el valor de la pila del nombre de la puerta y nos ponga el que le pongamos al crear la propia entidad
    return self.nombre 
  
  def entrar(self, alguien):
        if self.abierta:
            # Si el bicho viene del lado1, va al lado2 y viceversa
            if alguien.posicion == self.lado1:
                self.lado2.entrar_habitacion(alguien)
            else:
                self.lado1.entrar_habitacion(alguien)
        else:
            print(f"La {self.nombre} está cerrada. ¡PUM! ({alguien} se ha chocado)")
    






