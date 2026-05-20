import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.Entidades.Bicho import Bicho_Clase
from Laberinto26.Entidades.Perezoso import Perezoso
from Laberinto26.Entidades.Agresivo import Agresivo

class TestEstados(unittest.TestCase):
    def test_perezoso_mode(self):
        modo = Perezoso()
        bicho = Bicho_Clase(modo=modo, nombre="Bicho Perezoso")
        
        self.assertTrue(bicho.esPerezoso())
        self.assertFalse(bicho.esAgresivo())

    def test_agresivo_mode(self):
        modo = Agresivo()
        bicho = Bicho_Clase(modo=modo, nombre="Bicho Agresivo")
        
        self.assertTrue(bicho.esAgresivo())
        self.assertFalse(bicho.esPerezoso())

if __name__ == '__main__':
    unittest.main()
