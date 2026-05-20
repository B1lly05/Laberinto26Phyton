import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Laberinto26.ElementosFisicos.Puerta import Puerta_Clase
from Laberinto26.ElementosFisicos.Bomba import Bomba
from Laberinto26.ElementosFisicos.BombaVeneno import BombaVeneno
from Laberinto26.Visitor.VisitorAbrirPuertas import VisitorAbrirPuertas
from Laberinto26.Visitor.VisitorCerrarPuertas import VisitorCerrarPuertas
from Laberinto26.Visitor.VisitorActivarBombas import VisitorActivarBombas
from Laberinto26.Visitor.VisitorDesactivarBombas import VisitorDesactivarBombas

class TestVisitor(unittest.TestCase):
    def test_visitor_puertas(self):
        p = Puerta_Clase()
        self.assertFalse(p.estaAbierta())
        
        # Test Open Visitor
        v_open = VisitorAbrirPuertas()
        p.aceptar(v_open)
        self.assertTrue(p.estaAbierta())
        
        # Test Close Visitor
        v_close = VisitorCerrarPuertas()
        p.aceptar(v_close)
        self.assertFalse(p.estaAbierta())

    def test_visitor_bombas(self):
        bm = Bomba()
        self.assertTrue(bm.activa)
        
        # Test Deactivate Visitor
        v_deact = VisitorDesactivarBombas()
        bm.aceptar(v_deact)
        self.assertFalse(bm.activa)
        
        # Test Activate Visitor
        v_act = VisitorActivarBombas()
        bm.aceptar(v_act)
        self.assertTrue(bm.activa)

    def test_visitor_bomba_veneno(self):
        bm = BombaVeneno()
        self.assertTrue(bm.activa)
        
        # Test Deactivate
        v_deact = VisitorDesactivarBombas()
        bm.aceptar(v_deact)
        self.assertFalse(bm.activa)

if __name__ == '__main__':
    unittest.main()
