class Orientacion_Clase:
    instancias = {}

    #Este metodo lo que hara es comprobar si se ha creado una instancia, si se ha creado se redirige a ella misma
    def __new__(cls):
        if cls not in cls.instancias:
            cls.instancias[cls] = super().__new__(cls)
        return cls.instancias[cls]

    def caminar(self, un_bicho):
        pass

    def poner_elemento(self, un_em, un_cont):
        pass




class Norte(Orientacion_Clase):
    def caminar(self, un_bicho):
        # Traducido del código del profe: em := unBicho posicion norte. em entrar: unBicho
        habitacion_actual = un_bicho.posicion
        elemento_al_norte = habitacion_actual.norte 
        elemento_al_norte.entrar(un_bicho)

    def poner_elemento(self, un_em, un_cont):
        # Traducido: unCont norte: unEM
        un_cont.norte = un_em

    def __str__(self):
        return "Norte"


class Sur(Orientacion_Clase):
    def caminar(self, un_bicho):
        # Traducido del código del profe: em := unBicho posicion sur. em entrar: unBicho
        habitacion_actual = un_bicho.posicion
        elemento_al_sur = habitacion_actual.sur 
        elemento_al_sur.entrar(un_bicho)

    def poner_elemento(self, un_em, un_cont):
        # Traducido: unCont sur: unEM
        un_cont.sur = un_em

    def __str__(self):
        return "Sur"

 


class Este(Orientacion_Clase):
    def caminar(self, un_bicho):
        # Traducido del código del profe: em := unBicho posicion este. em entrar: unBicho
        habitacion_actual = un_bicho.posicion
        elemento_al_este = habitacion_actual.este
        elemento_al_este.entrar(un_bicho)

    def poner_elemento(self, un_em, un_cont):
        # Traducido: unCont este: unEM
        un_cont.este = un_em

    def __str__(self):
        return "Este"


class Oeste(Orientacion_Clase):
    def caminar(self, un_bicho):
        # Traducido del código del profe: em := unBicho posicion oeste. em entrar: unBicho
        habitacion_actual = un_bicho.posicion
        elemento_al_oeste = habitacion_actual.oeste
        elemento_al_oeste.entrar(un_bicho)

    def poner_elemento(self, un_em, un_cont):
        # Traducido: unCont oeste: unEM
        un_cont.oeste = un_em

    def __str__(self):
        return "Oeste"