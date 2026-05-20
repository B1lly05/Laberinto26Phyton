import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.ElementosFisicos.Armario import Armario_Clase
from Laberinto26.ElementosFisicos.ArmarioBombaVeneno import ArmarioBombaVeneno
from Laberinto26.Entidades.Bicho import Bicho_Clase

class TestArmarios(unittest.TestCase):
    def test_armario_normal(self):
        arm = Armario_Clase(1)
        self.assertEqual(arm.num, 1)
        self.assertEqual(getattr(arm, 'abierto', False), False)
        
    def test_armario_bomba_veneno(self):
        arm = ArmarioBombaVeneno(2)
        self.assertEqual(arm.num, 2)
        self.assertEqual(arm.EsArmarioBombaVeneno(), True)
        self.assertEqual(arm.activa, True)
        self.assertEqual(arm.abierto, False)
        
        player = Bicho_Clase(nombre="Hollow Knight")
        arm.entrar(player)
        self.assertEqual(player.estaVivo(), True)

if __name__ == '__main__':
    unittest.main()
