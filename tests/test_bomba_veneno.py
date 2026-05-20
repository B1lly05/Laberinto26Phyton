import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.ElementosFisicos.BombaVeneno import BombaVeneno
from Laberinto26.Entidades.Bicho import Bicho_Clase

class TestBombaVeneno(unittest.TestCase):
    def test_bomba_veneno_explosion(self):
        bomba = BombaVeneno()
        self.assertTrue(bomba.EsBomba())
        self.assertTrue(bomba.EsBombaVeneno())
        self.assertTrue(bomba.activa)
        
        player = Bicho_Clase(nombre="Hollow Knight")
        player.vidas = 50
        
        bomba.entrar(player)
        self.assertEqual(player.vidas, 35)
        self.assertFalse(bomba.activa)
        
        bomba.entrar(player)
        self.assertEqual(player.vidas, 35)

if __name__ == '__main__':
    unittest.main()
