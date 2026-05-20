import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.Juego import Juego_Clase
from Laberinto26.Entidades.Bicho import Bicho_Clase

class TestJuego(unittest.TestCase):
    def test_juego_initialization(self):
        juego = Juego_Clase()
        self.assertIsNone(juego.laberinto)
        self.assertIsNone(juego.personaje)
        self.assertEqual(len(juego.bichos), 0)
        
        # Assign personaje
        prota = Bicho_Clase(nombre="Hollow Knight")
        juego.personaje = prota
        self.assertEqual(juego.personaje.nombre, "Hollow Knight")

if __name__ == '__main__':
    unittest.main()
