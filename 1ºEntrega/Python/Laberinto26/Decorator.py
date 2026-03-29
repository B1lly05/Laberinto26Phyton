from .Hoja import Hoja_Clase

class Decorator_Clase(Hoja_Clase):
    def __init__(self):
        super().__init__()
        self.em = None
    

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

    def entrar(self, alguien):      # Si entra en contacto con una bomba activa le quitará vida 
        if self.activa:
            print(f"¡BOMBA! {alguien} ha pisado una trampa explosiva.")
            alguien.vidas -= 50
            
            if alguien.vidas > 0:
                print(f"A {alguien} le quedan {alguien.vidas} vidas.")
            else:
                alguien.vidas = 0  # Aseguramos que no queden en negativo
                alguien.posicion = None # <-- Esto hace que desaparezca del mapa
                print(f"{alguien} ha muerto por una explosión y se ha desintegrado.")    
        else:
             print(f"{alguien} ha pasado cerca de una bomba inactiva.")
