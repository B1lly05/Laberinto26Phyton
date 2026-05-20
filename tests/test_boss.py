import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26_builder.LaberintoBuilder import LaberintoBuilder_Clase

class TestBoss(unittest.TestCase):
    def test_guardian_stats(self):
        builder = LaberintoBuilder_Clase()
        builder.fabricar_laberinto()
        builder.fabricar_juego()
        builder.fabricar_habitacion(13)
        builder.fabricar_bicho_modo_posicion("Guardian", 13)
        
        bichos = builder.juego.bichos
        self.assertEqual(len(bichos), 1)
        
        guardian = bichos[0]
        self.assertEqual(guardian.nombre, "Guardian del Laberinto")
        self.assertEqual(guardian.vidas, 250)
        self.assertEqual(guardian.poder, 25)

if __name__ == '__main__':
    unittest.main()
