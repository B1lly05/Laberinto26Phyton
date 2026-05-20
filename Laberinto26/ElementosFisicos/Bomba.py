from Laberinto26.ElementosFisicos.Decorator import Decorator_Clase

class Bomba(Decorator_Clase):
    def __init__(self):
        super().__init__()
        self.activa = True

    def activar_bomba(self):
        print("Bomba activada")  
        self.activa = True
 
    def desactivar_bomba(self):
        print("Bomba desactivada")  
        self.activa = False

    def EsBomba(self):
        return True

    def entrar(self, alguien):      
        if self.activa:
            print(f"¡BOMBA! {alguien} ha pisado una trampa explosiva.")
            alguien.vidas -= 15
            
            if alguien.vidas > 0:
                print(f"A {alguien} le quedan {alguien.vidas} vidas.")
            else:
                alguien.vidas = 0  
                alguien.posicion = None 
                print(f"{alguien} ha muerto por una explosión y se ha desintegrado.")    
        else:
             print(f"{alguien} ha pasado cerca de una bomba inactiva.")

    def aceptar(self, visitor):
        visitor.visitar_bomba(self)
