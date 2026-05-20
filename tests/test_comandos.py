import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.Comandos.AtacarComando import AtacarComando
from Laberinto26.Comandos.UsarPocionComando import UsarPocionComando
from Laberinto26.Comandos.InteractuarComando import InteractuarComando

class FakePlayer:
    def __init__(self):
        self.x = 100
        self.y = 100

class FakeInterfaz:
    def __init__(self):
        self.ataques_realizados = 0
        self.inventario = {"llave": 0, "espada_olimpo": 0, "pocion_salud": 1, "armadura": 0}
        self.prota = type('Prota', (object,), {'vidas': 20})()
        self.player = FakePlayer()
        self.floating_texts = []
        self.particles = []
        self.hab_actual = type('Hab', (object,), {'hijos': [], 'num': 1})()
        self.room_floor_items = {}

    def _realizar_ataque(self):
        self.ataques_realizados += 1

class TestComandos(unittest.TestCase):
    def test_atacar_comando(self):
        interfaz = FakeInterfaz()
        cmd = AtacarComando(interfaz)
        cmd.ejecutar()
        self.assertEqual(interfaz.ataques_realizados, 1)

    def test_usar_pocion_comando(self):
        interfaz = FakeInterfaz()
        cmd = UsarPocionComando(interfaz)
        cmd.ejecutar()
        self.assertEqual(interfaz.inventario["pocion_salud"], 0)
        self.assertEqual(interfaz.prota.vidas, 50)

if __name__ == '__main__':
    unittest.main()
