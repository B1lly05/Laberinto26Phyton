import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.Entidades.Bicho import Bicho_Clase
from Laberinto26.ElementosFisicos.Llave import Llave
from Laberinto26.ElementosFisicos.PocionSalud import PocionSalud
from Laberinto26.ElementosFisicos.EspadaOlimpo import EspadaOlimpo
from Laberinto26.ElementosFisicos.Armadura import Armadura_Clase

class TestLoot(unittest.TestCase):
    def test_llave_entrar(self):
        player = Bicho_Clase(nombre="Hollow Knight")
        llave = Llave()
        llave.entrar(player)
        self.assertEqual(player.nombre, "Hollow Knight")

    def test_pocion_salud_entrar(self):
        player = Bicho_Clase(nombre="Hollow Knight")
        pocion = PocionSalud()
        pocion.entrar(player)
        self.assertEqual(player.estaVivo(), True)

    def test_espada_entrar(self):
        player = Bicho_Clase(nombre="Hollow Knight")
        espada = EspadaOlimpo()
        espada.entrar(player)
        self.assertEqual(player.poder, 10)

    def test_armadura_entrar(self):
        player = Bicho_Clase(nombre="Hollow Knight")
        armadura = Armadura_Clase()
        armadura.entrar(player)
        self.assertTrue(armadura.EsArmadura())

if __name__ == '__main__':
    unittest.main()

