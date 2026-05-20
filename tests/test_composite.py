import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.ElementosFisicos.Habitacion import Habitacion_Clase
from Laberinto26.ElementosFisicos.Llave import Llave
from Laberinto26.ElementosFisicos.Bomba import Bomba
from Laberinto26.ElementosFisicos.BombaVeneno import BombaVeneno

class TestComposite(unittest.TestCase):
    def test_habitacion_composite_structure(self):
        hab = Habitacion_Clase(5)
        self.assertEqual(hab.num, 5)
        self.assertEqual(len(hab.hijos), 0)
        
        # Add leaves
        k = Llave()
        b = Bomba()
        bv = BombaVeneno()
        
        hab.agregar_hijo(k)
        hab.agregar_hijo(b)
        hab.agregar_hijo(bv)
        
        self.assertEqual(len(hab.hijos), 3)
        self.assertIn(k, hab.hijos)
        self.assertIn(b, hab.hijos)
        self.assertIn(bv, hab.hijos)

if __name__ == '__main__':
    unittest.main()
