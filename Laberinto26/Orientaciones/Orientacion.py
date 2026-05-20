class Orientacion_Clase:
    instancias = {}

    def __new__(cls):
        if cls not in cls.instancias:
            cls.instancias[cls] = super().__new__(cls)
        return cls.instancias[cls]

    def caminar(self, un_bicho):
        pass

    def poner_elemento(self, un_em, un_cont):
        pass
