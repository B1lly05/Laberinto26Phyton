
import sys
import os
import tkinter as tk
from tkinter import font as tkfont
import math
import threading
import time
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from PIL import Image, ImageTk, ImageFilter, ImageEnhance
    PIL_OK = True
except ImportError:
    PIL_OK = False

from Laberinto26_builder.VistaLaberinto import VistaLaberinto_Clase
from Laberinto26.Orientaciones.Norte import Norte
from Laberinto26.Orientaciones.Sur import Sur
from Laberinto26.Orientaciones.Este import Este
from Laberinto26.Orientaciones.Oeste import Oeste

# ── Tamaños de ventana y habitación ──────────────────────────────────────────
WIN_W, WIN_H = 1120, 720
ROOM_X, ROOM_Y = 40, 50
ROOM_W, ROOM_H = 760, 520
TILE = 40                # tamaño de ladrillo/suelo
DOOR_W, DOOR_H = 80, 40
PLAYER_SPEED = 4.5
PLAYER_SIZE = 52

# Tamaños de bichos diferenciados según solicitud:
MONSTER_SIZE_AGR = 160  # Agresivo (mazo): ¡GIGANTESCO! (150px - 200px)
MONSTER_SIZE_PER = 30   # Perezoso (escarabajo): ¡Pequeñín!
GUARDIAN_SIZE = 280     # BOSS: El Guardián del Laberinto

HP_BAR_W = 50
HP_BAR_H = 7

# Colores
C_BG        = "#080810"  # Fondo oscuro profundo
C_WALL      = "#2e2014"  # Ladrillo oscuro
C_WALL_LT   = "#4d3420"  # Resalte de ladrillo
C_FLOOR     = "#241910"  # Suelo tierra oscuro
C_FLOOR_LT  = "#332417"  # Suelo tierra claro
C_DOOR_OPEN = "#05050a"
C_DOOR_FRAME= "#4d3420"
C_DOOR_WOOD = "#664024"
C_DOOR_KNOB = "#cda236"
C_HUD_BG    = "#140c0c"
C_HP_RED    = "#df2020"
C_HP_GREEN  = "#20df40"
C_HP_BACK   = "#2b0a0a"
C_ROOM_NUM  = "#e5c158"

# Coordenadas de mapa tal como se define en Main.py
MAP_COORDS = {
    14: (5, 4),
    13: (4, 4),
    12: (3, 4),
    10: (3, 0),
    11: (3, 1),
    9:  (2, 1),
    6:  (2, 3),
    7:  (2, 4),
    8:  (2, 5),
    2:  (1, 0),
    3:  (1, 1),
    4:  (1, 2),
    5:  (1, 3),
    1:  (0, 1),
    15: (0, 3),
    16: (0, 4),
    18: (0, 5)
}


# ─────────────────────────────────────────────────────────────────────────────
class FloatingText:
    def __init__(self, x, y, text, color, font=("Consolas", 14, "bold")):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.life = 60  # Duración en frames

    def update(self):
        self.y -= 1.2
        self.life -= 1

    def draw(self, canvas):
        canvas.create_text(self.x, self.y, text=self.text, fill=self.color,
                          font=self.font, tags=("floating",))


# ─────────────────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, vx, vy, color, size, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95
        self.life -= 1

    def draw(self, canvas):
        canvas.create_oval(self.x - self.size, self.y - self.size,
                           self.x + self.size, self.y + self.size,
                           fill=self.color, outline="", tags=("particle",))


# ─────────────────────────────────────────────────────────────────────────────
class Renderer:
    """Dibuja todos los elementos del juego en el Canvas."""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.assets: dict[str, tk.PhotoImage | ImageTk.PhotoImage] = {}
        self._load_assets()

    # ── Carga de imágenes con transparencia real ──────────────────────────────
    def _load_assets(self):
        base = os.path.join(os.path.dirname(__file__), "assets")
        specs = {
            "prota":    ("prota.png",    PLAYER_SIZE,  PLAYER_SIZE),
            "agresivo": ("agresivo.png", MONSTER_SIZE_AGR, MONSTER_SIZE_AGR),
            "perezoso": ("perezoso.png", MONSTER_SIZE_PER, MONSTER_SIZE_PER),
            "guardian": ("guardian.png", GUARDIAN_SIZE, GUARDIAN_SIZE),
        }
        for key, (fname, w, h) in specs.items():
            path = os.path.join(base, fname)
            if PIL_OK and os.path.exists(path):
                img = Image.open(path)
                img = img.convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)
                self.assets[key] = ImageTk.PhotoImage(img)
            else:
                self.assets[key] = None

    def draw_background(self):
        self.canvas.create_rectangle(0, 0, WIN_W, WIN_H, fill=C_BG, outline="")

    # ── Panel Lateral Derecho y HUD ──────────────────────────────────────────
    def draw_sidebar(self, prota, active_room, rooms_map, inventario=None):
        c = self.canvas
        sx, sy, sw, sh = 840, 0, 280, WIN_H

        # ── Fondo principal del panel (Hollow Knight: oscuro profundo con borde fino) ──
        c.create_rectangle(sx, sy, sx + sw, sy + sh, fill="#060811", outline="")
        # Borde izquierdo elegante (línea fina plateada como en HK)
        c.create_line(sx, sy, sx, sy + sh, fill="#3a4a6a", width=2)
        # Patrón decorativo superior (motivo de espinas/ramas HK)
        for i in range(0, sw, 14):
            c.create_line(sx + i, sy + 2, sx + i + 7, sy + 8, fill="#1a2035", width=1)
            c.create_line(sx + i + 7, sy + 8, sx + i + 14, sy + 2, fill="#1a2035", width=1)

        # ═══════════ TÍTULO "HOLLOW KNIGHT" ═══════════
        title_y = sy + 30
        # Sombra del título
        c.create_text(sx + sw // 2 + 1, title_y + 1, text="HOLLOW KNIGHT",
                      fill="#0a0f1a", font=("Consolas", 16, "bold"))
        c.create_text(sx + sw // 2, title_y, text="HOLLOW KNIGHT",
                      fill="#c8d8f0", font=("Consolas", 16, "bold"))
        # Línea decorativa doble bajo el título
        c.create_line(sx + 30, title_y + 16, sx + sw - 30, title_y + 16, fill="#2a3a5a", width=1)
        c.create_line(sx + 50, title_y + 19, sx + sw - 50, title_y + 19, fill="#1a2a40", width=1)

        # ═══════════ SALUD (Estilo Hollow Knight - Máscaras) ═══════════
        hp_section_y = title_y + 38
        armor_lvl = inventario.get("armadura", 0) if inventario else 0
        max_hp = 50 + armor_lvl * 25
        hp_pct = max(0.0, prota.vidas / max_hp)

        c.create_text(sx + 20, hp_section_y, anchor="w", text="SALUD",
                      fill="#7a8aaa", font=("Consolas", 9, "bold"))

        # Barra de vida estilo HK (contenedor fino, relleno blanco-azulado)
        bar_x = sx + 20
        bar_y = hp_section_y + 15
        bar_w = sw - 40
        bar_h = 14
        # Contenedor de la barra (borde plateado)
        c.create_rectangle(bar_x - 1, bar_y - 1, bar_x + bar_w + 1, bar_y + bar_h + 1,
                           fill="", outline="#3a4a6a", width=1)
        c.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + bar_h,
                           fill="#0a0e18", outline="")
        # Relleno de vida (blanco-azulado brillante HK)
        fill_w = int(bar_w * hp_pct)
        if hp_pct > 0.5:
            hp_color = "#e0eaff"  # Blanco azulado sano
        elif hp_pct > 0.25:
            hp_color = "#ff8844"  # Naranja dañado
        else:
            hp_color = "#ff3333"  # Rojo crítico
        if fill_w > 0:
            c.create_rectangle(bar_x, bar_y, bar_x + fill_w, bar_y + bar_h,
                               fill=hp_color, outline="")
            # Brillo interior de la barra
            c.create_rectangle(bar_x, bar_y + 1, bar_x + fill_w, bar_y + 4,
                               fill="#ffffff", outline="", stipple="gray25")

        # HP numérico centrado en la barra
        c.create_text(bar_x + bar_w // 2, bar_y + bar_h // 2,
                      text=f"{prota.vidas} / {max_hp}",
                      fill="#0a0e18" if hp_pct > 0.5 else "#ffffff",
                      font=("Consolas", 8, "bold"), anchor="center")

        # Indicador de armadura (si equipada)
        if armor_lvl > 0:
            c.create_text(sx + sw - 20, bar_y + bar_h + 12, anchor="e",
                          text=f"🛡️ Pechera Lvl {armor_lvl}",
                          fill="#8866cc", font=("Consolas", 8, "bold"))

        # ═══════════ LLAVES Y POCIONES ═══════════
        items_y = bar_y + bar_h + 30
        c.create_line(sx + 20, items_y - 8, sx + sw - 20, items_y - 8, fill="#1a2a40", width=1)

        llaves = inventario.get("llave", 0) if inventario else 0
        pociones = inventario.get("pocion_salud", 0) if inventario else 0
        espada_lvl = inventario.get("espada_olimpo", 0) if inventario else 0

        # Llaves (grande y prominente)
        c.create_text(sx + 25, items_y + 5, anchor="w", text="🔑",
                      font=("Consolas", 14))
        c.create_text(sx + 50, items_y + 5, anchor="w", text=f"x{llaves}",
                      fill="#ffd700", font=("Consolas", 13, "bold"))
        c.create_text(sx + 90, items_y + 5, anchor="w", text="Llaves",
                      fill="#7a8aaa", font=("Consolas", 9))

        # Pociones
        c.create_text(sx + 155, items_y + 5, anchor="w", text="🧪",
                      font=("Consolas", 14))
        c.create_text(sx + 180, items_y + 5, anchor="w", text=f"x{pociones}",
                      fill="#ff5555", font=("Consolas", 13, "bold"))

        # Espada (indicador compacto)
        if espada_lvl > 0:
            sword_col = "#20df40" if espada_lvl == 5 else "#00ccff"
            c.create_text(sx + 25, items_y + 28, anchor="w",
                          text=f"⚔ Espada Lvl {espada_lvl}",
                          fill=sword_col, font=("Consolas", 9, "bold"))
            if espada_lvl == 5:
                c.create_text(sx + 165, items_y + 28, anchor="w",
                              text="VENENO",
                              fill="#20df40", font=("Consolas", 8, "bold"))

        # ═══════════ MINI-MAPA ═══════════
        map_section_y = items_y + 50
        c.create_line(sx + 20, map_section_y, sx + sw - 20, map_section_y, fill="#1a2a40", width=1)
        c.create_text(sx + sw // 2, map_section_y + 16, text="MAPA",
                      fill="#c8d8f0", font=("Consolas", 12, "bold"))
        # Línea decorativa bajo "MAPA"
        c.create_line(sx + 80, map_section_y + 28, sx + sw - 80, map_section_y + 28, fill="#1a2a40", width=1)

        # ── Renderizado del Mini-Mapa ──
        mx_start = sx + 30
        my_start = map_section_y + 38
        grid_size = 30

        # Líneas de conexión entre habitaciones (puertas)
        for num, coord in MAP_COORDS.items():
            r, c_index = coord
            px = mx_start + c_index * grid_size + 10
            py = my_start + (5 - r) * grid_size + 10

            hab_obj = None
            for child in rooms_map:
                if child.num == num:
                    hab_obj = child
                    break

            if hab_obj:
                directions = [(Norte(), 0, -1), (Sur(), 0, 1), (Este(), 1, 0), (Oeste(), -1, 0)]
                for ori, ox, oy in directions:
                    el = hab_obj.obtener_elemento(ori)
                    if el and getattr(el, 'EsPuerta', lambda: False)():
                        tx = px + ox * grid_size
                        ty = py + oy * grid_size
                        c.create_line(px, py, tx, ty, fill="#1c2848", width=2)

        # Celdas de habitaciones
        for num, coord in MAP_COORDS.items():
            r, c_index = coord
            px = mx_start + c_index * grid_size
            py = my_start + (5 - r) * grid_size

            is_active = (active_room and active_room.num == num)

            if is_active:
                # Sala actual: blanco brillante con glow
                c.create_rectangle(px - 1, py - 1, px + 23, py + 23,
                                   fill="", outline="#c8d8f0", width=1)
                box_color = "#e0eaff"
                text_color = "#060811"
            else:
                box_color = "#121828"
                text_color = "#5a6a8a"

            c.create_rectangle(px, py, px + 20, py + 20,
                               fill=box_color, outline="#2a3a5a", width=1)
            c.create_text(px + 10, py + 10, text=f"{num}",
                          fill=text_color, font=("Consolas", 7, "bold"))

        # Sala actual indicador
        if active_room:
            c.create_text(sx + sw // 2, my_start + 6 * grid_size + 10,
                          text=f"Sala {active_room.num}",
                          fill="#c8d8f0", font=("Consolas", 9, "bold"))

        # ═══════════ CONTROLES ═══════════
        ctrl_section_y = my_start + 6 * grid_size + 30
        c.create_line(sx + 20, ctrl_section_y, sx + sw - 20, ctrl_section_y, fill="#1a2a40", width=1)
        c.create_text(sx + sw // 2, ctrl_section_y + 14, text="CONTROLES",
                      fill="#c8d8f0", font=("Consolas", 11, "bold"))

        controls = [
            ("WASD", "Mover"),
            ("ESPACIO", "Atacar ⚔"),
            ("I", "Inventario"),
            ("E", "Armarios 🚪"),
            ("H / U", "Poción 🧪"),
        ]

        ctrl_y = ctrl_section_y + 32
        for idx, (btn, desc) in enumerate(controls):
            row_y = ctrl_y + idx * 18
            # Tecla en recuadro estilo HK
            c.create_rectangle(sx + 22, row_y - 7, sx + 70, row_y + 7,
                               fill="#121828", outline="#2a3a5a", width=1)
            c.create_text(sx + 46, row_y, text=btn,
                          fill="#c8d8f0", font=("Consolas", 7, "bold"))
            c.create_text(sx + 78, row_y, anchor="w", text=desc,
                          fill="#5a6a8a", font=("Consolas", 8))

        # ═══════════ OBJETIVO ═══════════
        obj_y = ctrl_y + len(controls) * 18 + 12
        c.create_line(sx + 20, obj_y, sx + sw - 20, obj_y, fill="#1a2a40", width=1)
        c.create_text(sx + sw // 2, obj_y + 14, text="OBJETIVO",
                      fill="#ffd700", font=("Consolas", 11, "bold"))
        c.create_text(sx + sw // 2, obj_y + 34, text="Explora el laberinto",
                      fill="#7a8aaa", font=("Consolas", 8))
        c.create_text(sx + sw // 2, obj_y + 48, text="Llega a la Sala 14",
                      fill="#c8d8f0", font=("Consolas", 9, "bold"))
        c.create_text(sx + sw // 2, obj_y + 62, text="y sobrevive a los monstruos.",
                      fill="#7a8aaa", font=("Consolas", 8))

        # ═══════════ INVENTARIO SHORTCUT ═══════════
        c.create_text(sx + sw // 2, sy + sh - 20,
                      text="[I] Inventario completo",
                      fill="#3a4a6a", font=("Consolas", 8, "bold"))

        # Patrón decorativo inferior (motivo de espinas/ramas HK)
        bottom_y = sy + sh - 5
        for i in range(0, sw, 14):
            c.create_line(sx + i, bottom_y, sx + i + 7, bottom_y - 6, fill="#1a2035", width=1)
            c.create_line(sx + i + 7, bottom_y - 6, sx + i + 14, bottom_y, fill="#1a2035", width=1)

    # ── Habitación (Isaac-style) ──────────────────────────────────────────────
    def draw_room(self, habitacion, ox=0, oy=0, floor_items=None):
        """ox,oy = offset de desplazamiento para la animación de slide"""
        c = self.canvas
        rx = ROOM_X + ox
        ry = ROOM_Y + oy
        rw, rh = ROOM_W, ROOM_H

        # ── Suelo base (tierra cálida tipo Isaac) ──
        c.create_rectangle(rx + TILE, ry + TILE, rx + rw - TILE, ry + rh - TILE,
                           fill="#5a3a28", outline="")

        # ── Tiles de suelo con variación procedural ──
        FTILE = 48
        for gy in range(ry + TILE, ry + rh - TILE, FTILE):
            for gx in range(rx + TILE, rx + rw - TILE, FTILE):
                random.seed(gx * 31 + gy * 17 + habitacion.num)
                shade = random.choice(["#5a3a28", "#4e3022", "#623e2c", "#533625"])
                c.create_rectangle(gx, gy, gx + FTILE, gy + FTILE, fill=shade, outline="#3d2518", width=1)
                # Marcas de tierra (grietas, manchas)
                if random.random() < 0.18:
                    mx = gx + random.randint(6, FTILE - 6)
                    my = gy + random.randint(6, FTILE - 6)
                    c.create_oval(mx - 4, my - 2, mx + 4, my + 2, fill="#3a2216", outline="")
                if random.random() < 0.12:
                    mx = gx + random.randint(5, FTILE - 5)
                    my = gy + random.randint(5, FTILE - 5)
                    c.create_line(mx, my, mx + random.randint(5,12), my + random.randint(-3,3),
                                  fill="#3a2216", width=1)

        # ── Rocas en esquinas estilo Isaac ──
        corner_size = TILE + 16
        corners = [
            (rx + TILE, ry + TILE),
            (rx + rw - TILE - corner_size, ry + TILE),
            (rx + TILE, ry + rh - TILE - corner_size),
            (rx + rw - TILE - corner_size, ry + rh - TILE - corner_size),
        ]
        for (cx_, cy_) in corners:
            # Roca oscura con highlight
            c.create_oval(cx_, cy_, cx_ + corner_size, cy_ + corner_size,
                          fill="#2e2020", outline="#1a1212", width=2)
            c.create_oval(cx_ + 4, cy_ + 4, cx_ + corner_size - 8, cy_ + corner_size - 8,
                          fill="#3a2828", outline="")
            # Highlight de roca (brillo superior izquierdo)
            c.create_arc(cx_ + 6, cy_ + 6, cx_ + corner_size - 14, cy_ + corner_size - 14,
                         start=45, extent=90, style=tk.ARC, outline="#5a4040", width=2)

        # ── Rocas aleatorias en el interior (pocas) ──
        random.seed(habitacion.num * 99)
        for _ in range(3):
            bx = rx + TILE + random.randint(80, rw - 160)
            by = ry + TILE + random.randint(80, rh - 160)
            rs = random.randint(10, 18)
            c.create_oval(bx - rs, by - rs // 2, bx + rs, by + rs // 2,
                          fill="#2e2020", outline="#1a1212", width=1)

        # ── Muros de piedra/ladrillo ──
        self._draw_isaac_wall(rx, ry, rw, TILE, 'N')
        self._draw_isaac_wall(rx, ry + rh - TILE, rw, TILE, 'S')
        self._draw_isaac_wall(rx, ry, TILE, rh, 'W')
        self._draw_isaac_wall(rx + rw - TILE, ry, TILE, rh, 'E')

        # Número de habitación
        c.create_text(rx + TILE + 6, ry + TILE + 14, text=f"#{habitacion.num}",
                      fill=C_ROOM_NUM, font=("Consolas", 10, "bold"), anchor='w')

        # ── Puertas ──
        doors = {
            "Norte": (habitacion.obtener_elemento(Norte()), "N"),
            "Sur":   (habitacion.obtener_elemento(Sur()),   "S"),
            "Este":  (habitacion.obtener_elemento(Este()),  "E"),
            "Oeste": (habitacion.obtener_elemento(Oeste()), "O"),
        }
        for _, (elem, lado) in doors.items():
            self._draw_door(elem, lado, ox=ox, oy=oy)

        # ── Bombas según JSON ──
        pos_esquinas = [
            (rx + 160, ry + 130),
            (rx + rw - 160, ry + 130),
            (rx + 160, ry + rh - 130),
            (rx + rw - 160, ry + rh - 130)
        ]
        bombas = [h for h in habitacion.hijos if getattr(h, 'EsBomba', lambda: False)()]
        for idx, bomba in enumerate(bombas):
            if idx >= len(pos_esquinas):
                break
            
            # Distribuimos las bombas pseudo-aleatoriamente en diferentes esquinas y posiciones
            # según el número de la habitación para que no coincidan siempre en el mismo punto exacto.
            random.seed(habitacion.num * 47 + idx * 29)
            esquina_idx = (habitacion.num + idx) % len(pos_esquinas)
            bx_base, by_base = pos_esquinas[esquina_idx]
            
            # Desviación para distribuirlas aleatoriamente por la habitación
            bx_ = bx_base + random.randint(-50, 50)
            by_ = by_base + random.randint(-40, 40)
            
            # Guardar posición lógica (sin offset, para colisiones)
            bomba.x = bx_ - ox
            bomba.y = by_ - oy
            if getattr(bomba, 'activa', True):
                # 💣 Bomba oculta: se dibuja sutilmente camuflada como una baldosa de presión rota natural
                is_ven = getattr(bomba, 'EsBombaVeneno', lambda: False)()
                fill_color = "#1b2014" if is_ven else "#1f150e"
                outline_color = "#14180f" if is_ven else "#18100a"
                c.create_rectangle(bx_ - 24, by_ - 24, bx_ + 24, by_ + 24,
                                   fill=fill_color, outline=outline_color, width=1.2, tags=("bomba_visual",))
                
                # Faint dark cracks (looks like natural room stone texture lines)
                crack_color = "#0e120a" if is_ven else "#120a06"
                c.create_line(bx_ - 14, by_ - 8, bx_ + 6, by_ + 12, fill=crack_color, width=1)
                c.create_line(bx_ - 4, by_ + 10, bx_ + 14, by_ - 10, fill=crack_color, width=1)
            else:
                # Detonada o desactivada: Cráter negro/verdoso quemado y destruido
                is_ven = getattr(bomba, 'EsBombaVeneno', lambda: False)()
                crater_fill = "#051405" if is_ven else "#0e0a0a"
                crater_outline = "#153c15" if is_ven else "#2a1818"
                c.create_oval(bx_ - 15, by_ - 15, bx_ + 15, by_ + 15,
                              fill=crater_fill, outline=crater_outline, width=2, tags=("bomba_visual",))
                c.create_oval(bx_ - 7, by_ - 7, bx_ + 7, by_ + 7, fill="#080606" if not is_ven else "#051005", outline="")


        # ── Dibujar Armarios Físicos (Negros, en la pared Norte) ──
        armarios = [h for h in habitacion.hijos if h.__class__.__name__ in ('Armario_Clase', 'ArmarioBombaVeneno')]
        for arm in armarios:
            is_ven_arm = (arm.__class__.__name__ == 'ArmarioBombaVeneno')
            # Posición lógica (sin offset de animación)
            arm.x = (rx + ROOM_W // 3) - ox
            arm.y = (ry + TILE + 20) - oy
            
            ax = rx + ROOM_W // 3
            ay = ry + TILE + 20
            aw, ah = 56, 40
            
            # Sombra del armario
            c.create_oval(ax - aw//2, ay + ah//2 - 6, ax + aw//2, ay + ah//2 + 4, fill="#1c0f0a" if not is_ven_arm else "#081c08", outline="", tags=("armario_visual",))
            
            # Cuerpo negro/verdoso del armario
            body_fill = "#051a05" if is_ven_arm else "#0a0a0a"
            body_outline = "#20df40" if is_ven_arm else "#1c1c1c"
            c.create_rectangle(ax - aw//2, ay - ah//2, ax + aw//2, ay + ah//2,
                               fill=body_fill, outline=body_outline, width=2.5, tags=("armario_visual",))
            
            # Marco interior elegante
            inner_fill = "#031003" if is_ven_arm else "#121212"
            inner_outline = "#155015" if is_ven_arm else "#252525"
            c.create_rectangle(ax - aw//2 + 4, ay - ah//2 + 4, ax + aw//2 - 4, ay + ah//2 - 4,
                               fill=inner_fill, outline=inner_outline, width=1.5, tags=("armario_visual",))
            
            # Puertas (línea vertical central)
            c.create_line(ax, ay - ah//2 + 4, ax, ay + ah//2 - 4, fill="#104010" if is_ven_arm else "#2a2a2a", width=2, tags=("armario_visual",))
            
            # Pomos/tiradores dorados pequeños de las puertas
            pomo_color = "#32cd32" if is_ven_arm else "#ffd700"
            c.create_oval(ax - 4, ay - 2, ax - 1, ay + 1, fill=pomo_color, outline="", tags=("armario_visual",))
            c.create_oval(ax + 1, ay - 2, ax + 4, ay + 1, fill=pomo_color, outline="", tags=("armario_visual",))
            
            # Indicador de estado visual (si está abierto, dibujamos las puertas entreabiertas!)
            if getattr(arm, 'abierto', False):
                # Relleno interno vacío de armario abierto (verde tóxico / morado / negro)
                open_fill = "#020f02" if is_ven_arm else "#08040f"
                c.create_rectangle(ax - aw//2 + 6, ay - ah//2 + 6, ax + aw//2 - 6, ay + ah//2 - 6,
                                   fill=open_fill, outline="")
                # Puertas entreabiertas a los lados
                c.create_rectangle(ax - aw//2 - 8, ay - ah//2 + 4, ax - aw//2 + 2, ay + ah//2 - 4,
                                   fill=body_fill, outline=body_outline, width=1.5, tags=("armario_visual",))
                c.create_rectangle(ax + aw//2 - 2, ay - ah//2 + 4, ax + aw//2 + 8, ay + ah//2 - 4,
                                   fill=body_fill, outline=body_outline, width=1.5, tags=("armario_visual",))

        # ── Dibujar Items en el suelo ──
        if floor_items:
            for item in floor_items:
                ix = item["x"] + ox
                iy = item["y"] + oy
                tipo = item["tipo"]
                
                # Sombra del item
                c.create_oval(ix - 10, iy - 2, ix + 10, iy + 2, fill="#1c0f0a", outline="", tags=("item_shadow",))
                
                if tipo == "llave":
                    # Llave dorada brillante
                    c.create_oval(ix - 5, iy - 5, ix + 1, iy + 1, fill="#ffd700", outline="#b39200", width=1)
                    c.create_line(ix, iy, ix + 6, iy + 6, fill="#ffd700", width=2)
                    c.create_line(ix + 4, iy + 4, ix + 6, iy + 2, fill="#ffd700", width=2)
                    c.create_line(ix + 5, iy + 5, ix + 7, iy + 3, fill="#ffd700", width=2)
                elif tipo == "pocion":
                    # Pocima de salud brillante
                    c.create_polygon(ix - 3, iy + 5, ix + 3, iy + 5, ix + 5, iy - 1, ix - 5, iy - 1,
                                     fill="#ff1a1a", outline="#b30000", width=1)
                    c.create_rectangle(ix - 1, iy - 5, ix + 1, iy - 1, fill="#aaaaaa", outline="#555555")
                    c.create_oval(ix - 3, iy - 1, ix + 3, iy + 4, fill="#ff1a1a", outline="")
                    c.create_oval(ix - 1, iy, ix, iy + 1, fill="#ffffff", outline="")
                elif tipo == "espada":
                    # Espada del Olimpo brillante (celeste)
                    c.create_line(ix - 6, iy + 6, ix + 6, iy - 6, fill="#e6f7ff", width=2)
                    c.create_line(ix - 6, iy + 6, ix + 6, iy - 6, fill="#00bfff", width=1)
                    c.create_line(ix - 3, iy + 1, ix - 1, iy + 3, fill="#ffd700", width=2) # Guarda
                    c.create_oval(ix - 7, iy + 7, ix - 5, iy + 5, fill="#ffd700", outline="") # Pomo
                elif tipo == "armadura":
                    # Armadura Misterio del Laberinto (Pechera morada ribeteada en oro)
                    c.create_polygon(ix - 8, iy - 6, ix + 8, iy - 6, ix + 6, iy + 6, ix - 6, iy + 6,
                                     fill="#6a0dad", outline="#ffd700", width=1.5, tags=("item_visual",))
                    c.create_rectangle(ix - 3, iy - 10, ix + 3, iy - 6, fill="#6a0dad", outline="#ffd700", tags=("item_visual",))
                    c.create_line(ix - 6, iy - 2, ix + 6, iy - 2, fill="#ffd700", width=1, tags=("item_visual",))

    def _draw_isaac_wall(self, x, y, w, h, side):
        """Muro de piedra oscura estilo Isaac con bloques y sombra interna."""
        c = self.canvas
        # Fondo base del muro
        c.create_rectangle(x, y, x + w, y + h, fill="#1e1614", outline="")
        # Bloques de piedra
        bw = TILE if side in ('N', 'S') else TILE // 2
        bh = TILE // 2 if side in ('N', 'S') else TILE
        for row in range(y, y + h, bh):
            off = (bw // 2) if (((row - y) // bh) % 2 == 1) else 0
            for col in range(x - off, x + w, bw):
                bx_ = max(x, col)
                by_ = row
                ex_ = min(x + w, col + bw)
                ey_ = min(y + h, row + bh)
                if ex_ > bx_ and ey_ > by_:
                    c.create_rectangle(bx_, by_, ex_, ey_,
                                       fill="#2a1e1a", outline="#140e0c", width=1)
                    # Highlight de piedra (esquina sup-izq)
                    c.create_line(bx_ + 1, by_ + 1, ex_ - 2, by_ + 1, fill="#3a2a24", width=1)
                    c.create_line(bx_ + 1, by_ + 1, bx_ + 1, ey_ - 2, fill="#3a2a24", width=1)
        # Sombra interior (borde hacia dentro del suelo)
        if side == 'N':
            c.create_rectangle(x, y + h - 4, x + w, y + h, fill="#100a08", outline="")
        elif side == 'S':
            c.create_rectangle(x, y, x + w, y + 4, fill="#100a08", outline="")
        elif side == 'W':
            c.create_rectangle(x + w - 4, y, x + w, y + h, fill="#100a08", outline="")
        elif side == 'E':
            c.create_rectangle(x, y, x + 4, y + h, fill="#100a08", outline="")

    def _draw_brick_wall(self, x, y, w, h, horizontal=True):
        self._draw_isaac_wall(x, y, w, h, 'N' if horizontal else 'W')

    def _draw_door(self, elemento, lado, ox=0, oy=0):
        c = self.canvas
        rx = ROOM_X + ox
        ry = ROOM_Y + oy
        rw, rh = ROOM_W, ROOM_H
        cx = rx + rw // 2
        cy = ry + rh // 2

        es_puerta = elemento is not None and getattr(elemento, 'EsPuerta', lambda: False)()
        if not es_puerta:
            return

        abierta = getattr(elemento, 'estaAbierta', lambda: False)()

        if lado == "N":
            dx, dy = cx - DOOR_W // 2, ry
            dw, dh = DOOR_W, TILE
        elif lado == "S":
            dx, dy = cx - DOOR_W // 2, ry + rh - TILE
            dw, dh = DOOR_W, TILE
        elif lado == "E":
            dx, dy = rx + rw - TILE, cy - DOOR_W // 2
            dw, dh = TILE, DOOR_W
        else:
            dx, dy = rx, cy - DOOR_W // 2
            dw, dh = TILE, DOOR_W

        if abierta:
            c.create_rectangle(dx, dy, dx + dw, dy + dh,
                               fill=C_DOOR_OPEN, outline="")
            c.create_rectangle(dx, dy, dx + dw, dy + dh,
                               fill="", outline="#e5c158", width=2, dash=(6, 4))
        else:
            c.create_rectangle(dx, dy, dx + dw, dy + dh,
                               fill=C_DOOR_FRAME, outline=C_WALL_LT, width=2)
            inner_x, inner_y = dx + 4, dy + 4
            inner_w, inner_h = dw - 8, dh - 8
            c.create_rectangle(inner_x, inner_y, inner_x + inner_w, inner_y + inner_h,
                               fill=C_DOOR_WOOD, outline=C_DOOR_FRAME, width=1)
            if lado in ("N", "S"):
                mid = inner_y + inner_h // 2
                c.create_line(inner_x, mid, inner_x + inner_w, mid, fill=C_DOOR_FRAME, width=1)
            else:
                mid = inner_x + inner_w // 2
                c.create_line(mid, inner_y, mid, inner_y + inner_h, fill=C_DOOR_FRAME, width=1)
            kx, ky = dx + dw // 2, dy + dh // 2
            c.create_oval(kx - 4, ky - 4, kx + 4, ky + 4,
                          fill=C_DOOR_KNOB, outline="#8b6914", width=1)

    # ── Entidades y Enemigos ──────────────────────────────────────────────────
    def draw_entity(self, x, y, kind, vidas, nombre, max_vidas=50, label=None, bobbing=0, sleeping=False):
        c = self.canvas
        img = self.assets.get(kind)
        if kind == "prota":
            size = PLAYER_SIZE
        elif kind == "guardian":
            size = GUARDIAN_SIZE
        elif kind == "agresivo":
            size = MONSTER_SIZE_AGR
        else:
            size = MONSTER_SIZE_PER

        # y = centro vertical del sprite
        draw_y = y + (0 if sleeping else int(bobbing))

        # Sombra ovalada justo en los pies del sprite
        foot_y = draw_y + size // 2
        shadow_w = size // 2
        c.create_oval(x - shadow_w, foot_y - 4, x + shadow_w, foot_y + 4,
                      fill="#04020a", outline="", tags=("entity_shadow",))

        if img:
            c.create_image(x, draw_y, image=img, anchor="center", tags=("entity",))
        else:
            colors = {"prota": "#ffffff", "agresivo": "#ff3333", "perezoso": "#bb8855"}
            fc = colors.get(kind, "#aaaaaa")
            half = size // 2
            c.create_oval(x - half, draw_y - half, x + half, draw_y + half,
                          fill=fc, outline="white", width=2)

        if sleeping:
            c.create_text(x + size//3, draw_y - size//3, text="💤", font=("Consolas", 12))

        # Barra de vida: siempre debajo del sprite, usando draw_y para que siga el bobbing
        bar_y = draw_y + size // 2 + 6
        hp_pct = max(0.0, vidas / max_vidas)
        bar_w = max(40, min(80, size))
        c.create_rectangle(x - bar_w // 2, bar_y, x + bar_w // 2, bar_y + HP_BAR_H,
                           fill=C_HP_BACK, outline="#111", width=1)
        fill_w = int(bar_w * hp_pct)
        color = C_HP_GREEN if hp_pct > 0.4 else C_HP_RED
        if fill_w > 0:
            c.create_rectangle(x - bar_w // 2, bar_y, x - bar_w // 2 + fill_w, bar_y + HP_BAR_H,
                               fill=color, outline="")

        if label:
            c.create_text(x, bar_y + HP_BAR_H + 10, text=label,
                          fill="#c0b0a0", font=("Consolas", 9, "bold"))

    # ── Efecto de Espadazo (Corte de Luz) ──
    def draw_attack_slash(self, px, py, facing, timer_val, espada_level=0):
        c = self.canvas
        r = int(55 * 1.5) if espada_level > 0 else 55  # Rango visual un pelín menor con Espada del Olimpo
        angles = {
            'N': (45, 90),
            'S': (225, 90),
            'E': (315, 90),
            'O': (135, 90)
        }
        start_ang, extent_ang = angles.get(facing, (0, 90))
        
        # Color y estilo premium basado en el nivel de la espada
        if espada_level == 5:
            color_outer = "#20df40"  # Veneno tóxico verde brillante para nivel 5
            width_outer = 10
        elif espada_level > 0:
            color_outer = "#ffd700"  # Dorado brillante para niveles 1-4
            width_outer = 8
        else:
            color_outer = "#00ffff"  # Cyan original
            width_outer = 4
            
        color_inner = "#ffffff"
        
        c.create_arc(px - r - 4, py - r - 4, px + r + 4, py + r + 4,
                     start=start_ang, extent=extent_ang, style=tk.ARC,
                     outline=color_outer, width=width_outer, tags=("slash",))
        c.create_arc(px - r, py - r, px + r, py + r,
                     start=start_ang, extent=extent_ang, style=tk.ARC,
                     outline=color_inner, width=4 if espada_level > 0 else 2, tags=("slash",))


# ─────────────────────────────────────────────────────────────────────────────
class PlayerController:
    def __init__(self):
        self.x = WIN_W // 2 - 100
        self.y = WIN_H // 2 - 30
        self.vx = 0
        self.vy = 0
        self.keys: set[str] = set()
        self.facing = 'E'
        self.attack_timer = 0
        self.attack_cooldown = 0

        self.min_x = ROOM_X + TILE + PLAYER_SIZE // 2
        self.max_x = ROOM_X + ROOM_W - TILE - PLAYER_SIZE // 2
        self.min_y = ROOM_Y + TILE + PLAYER_SIZE // 2
        self.max_y = ROOM_Y + ROOM_H - TILE - PLAYER_SIZE // 2

    def key_down(self, key: str):
        self.keys.add(key.lower())

    def key_up(self, key: str):
        self.keys.discard(key.lower())

    def update(self):
        self.vx = 0
        self.vy = 0
        if "w" in self.keys or "up" in self.keys:
            self.vy = -PLAYER_SPEED
            self.facing = 'N'
        if "s" in self.keys or "down" in self.keys:
            self.vy = PLAYER_SPEED
            self.facing = 'S'
        if "a" in self.keys or "left" in self.keys:
            self.vx = -PLAYER_SPEED
            self.facing = 'O'
        if "d" in self.keys or "right" in self.keys:
            self.vx = PLAYER_SPEED
            self.facing = 'E'

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        self.x = max(self.min_x, min(self.max_x, self.x + self.vx))
        self.y = max(self.min_y, min(self.max_y, self.y + self.vy))

        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def check_door_transition(self, habitacion, main) -> str | None:
        cx = ROOM_X + ROOM_W // 2
        cy = ROOM_Y + ROOM_H // 2
        margen = PLAYER_SIZE // 2 + 10

        checks = {
            "N": (Norte(), self.y < ROOM_Y + TILE + margen, abs(self.x - cx) < DOOR_W // 2),
            "S": (Sur(),  self.y > ROOM_Y + ROOM_H - TILE - margen, abs(self.x - cx) < DOOR_W // 2),
            "E": (Este(), self.x > ROOM_X + ROOM_W - TILE - margen, abs(self.y - cy) < DOOR_W // 2),
            "O": (Oeste(), self.x < ROOM_X + TILE + margen, abs(self.y - cy) < DOOR_W // 2),
        }
        for dir_name, (dir_obj, cond_main, cond_align) in checks.items():
            if cond_main and cond_align:
                elem = habitacion.obtener_elemento(dir_obj)
                if elem and getattr(elem, 'EsPuerta', lambda: False)():
                    if getattr(elem, 'estaAbierta', lambda: False)():
                        return dir_name
                    else:
                        # Si está cerrada pero tenemos llaves, la abrimos automáticamente
                        if main.inventario["llave"] > 0:
                            main.inventario["llave"] -= 1
                            elem.abrir_puerta()
                            main.floating_texts.append(FloatingText(
                                self.x, self.y - 30, "¡Puerta abierta con llave! 🔑", "#ffff00", ("Consolas", 12, "bold")
                            ))
                            return dir_name
                        else:
                            # Mostrar aviso de puerta cerrada una vez cada poco
                            if main.anim_tick % 90 == 0:
                                main.floating_texts.append(FloatingText(
                                    self.x, self.y - 30, "Necesitas una llave 🔒", "#ff3333", ("Consolas", 12, "bold")
                                ))
        return None


# ─────────────────────────────────────────────────────────────────────────────
class BossBomb:
    """Proyectil de bomba naranja lanzada por el Guardián del Laberinto."""
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy) or 1.0
        speed = 3.5
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed
        self.life = 90  # Frames antes de explotar automáticamente
        self.exploded = False
        self.radius = 8

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.exploded = True

    def draw(self, canvas):
        if not self.exploded:
            # Bomba naranja brillante con estela
            canvas.create_oval(self.x - self.radius, self.y - self.radius,
                               self.x + self.radius, self.y + self.radius,
                               fill="#ff6600", outline="#ffaa00", width=2)
            # Brillo interior
            canvas.create_oval(self.x - 3, self.y - 3, self.x + 3, self.y + 3,
                               fill="#ffcc00", outline="")
            # Estela de humo
            canvas.create_oval(self.x - self.vx * 3 - 4, self.y - self.vy * 3 - 4,
                               self.x - self.vx * 3 + 4, self.y - self.vy * 3 + 4,
                               fill="#553311", outline="", stipple="gray50")


class MonsterAI:
    def __init__(self, bicho, is_agresivo: bool, is_guardian: bool = False):
        self.bicho = bicho
        self.is_agresivo = is_agresivo
        self.is_guardian = is_guardian
        if is_guardian:
            # El Guardián aparece en el centro de la sala
            self.x = ROOM_X + ROOM_W // 2
            self.y = ROOM_Y + ROOM_H // 2
        else:
            self.x = random.randint(ROOM_X + TILE + 120, ROOM_X + ROOM_W - TILE - 120)
            self.y = random.randint(ROOM_Y + TILE + 120, ROOM_Y + ROOM_H - TILE - 120)
        self.vx = random.choice([-1, 1]) * (2.2 if is_agresivo else 0.8)
        self.vy = random.choice([-1, 1]) * (2.2 if is_agresivo else 0.8)
        self.timer = 0
        self.last_hit_time = 0.0
        self.poison_ticks_left = 0
        self.last_poison_tick_time = 0.0
        # Guardian bomb system
        self.bomb_cooldown = 0
        self.bombs: list[BossBomb] = []

    def update(self, px, py):
        # El agresivo NUNCA se inmoviliza por dormir (los perezosos sí cuando su thread lo dicta)
        if not self.is_agresivo and not self.is_guardian and getattr(self.bicho, 'is_sleeping', False):
            self.vx = 0
            self.vy = 0
            return

        if self.is_guardian:
            # El Guardián se mueve lentamente hacia el jugador
            dx = px - self.x
            dy = py - self.y
            dist = math.hypot(dx, dy) or 1.0
            speed = 0.9
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed

            # Lanzar bombas naranjas periódicamente
            self.bomb_cooldown -= 1
            if self.bomb_cooldown <= 0:
                self.bomb_cooldown = random.randint(60, 120)  # Cada 1-2 segundos
                # Lanza bomba hacia el jugador con ligero offset aleatorio
                self.bombs.append(BossBomb(
                    self.x, self.y,
                    px + random.randint(-60, 60),
                    py + random.randint(-60, 60)
                ))

            # Actualizar bombas existentes
            for b in list(self.bombs):
                b.update()

        elif self.is_agresivo:
            dx = px - self.x
            dy = py - self.y
            dist = math.hypot(dx, dy) or 1.0
            speed = 1.8
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.timer += 1
            if self.timer > 100:
                self.timer = 0
                self.vx = random.choice([-0.8, 0.0, 0.8])
                self.vy = random.choice([-0.8, 0.0, 0.8])

        nx = self.x + self.vx
        ny = self.y + self.vy
        
        if self.is_guardian:
            size = GUARDIAN_SIZE
            margin = size // 6
        elif self.is_agresivo:
            size = MONSTER_SIZE_AGR
            margin = size // 4
        else:
            size = MONSTER_SIZE_PER
            margin = size // 2
        mn_x = ROOM_X + TILE + margin
        mx_x = ROOM_X + ROOM_W - TILE - margin
        mn_y = ROOM_Y + TILE + margin
        mx_y = ROOM_Y + ROOM_H - TILE - margin

        if nx < mn_x or nx > mx_x:
            self.vx *= -1
            nx = max(mn_x, min(mx_x, nx))
        if ny < mn_y or ny > mx_y:
            self.vy *= -1
            ny = max(mn_y, min(mx_y, ny))

        self.x, self.y = nx, ny


from Laberinto26.Comandos.AtacarComando import AtacarComando
from Laberinto26.Comandos.UsarPocionComando import UsarPocionComando
from Laberinto26.Comandos.InteractuarComando import InteractuarComando
class MainInterfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Laberinto26  ·  Hollow Knight 2D")
        self.root.resizable(False, False)
        self.root.configure(bg=C_BG)

        self.canvas = tk.Canvas(self.root, width=WIN_W, height=WIN_H,
                                bg=C_BG, highlightthickness=0)
        self.canvas.pack()

        self.renderer = Renderer(self.canvas)
        self.player = PlayerController()

        self.floating_texts: list[FloatingText] = []
        self.particles: list[Particle] = []
        self.screen_shake = 0
        self.anim_tick = 0
        self.blood_drips = [] # Efectos de sangre cayendo en muerte
        self.player_burn_ticks = 0  # Ticks de quemadura de bombas del Guardián
        self.player_burn_last_tick = 0.0  # Timestamp del último tick de quemadura

        self.juego = None
        self.prota = None
        self.hab_actual = None
        self.monsters: list[MonsterAI] = []
        self.transition_cooldown = 0
        self.running = True
        self.triggered_bombs = set()
        self.player_poison_ticks = 0
        self.player_poison_last_tick = 0.0

        # Sistema de Inventario e Items Físicos
        self.inventario = {"llave": 0, "espada_olimpo": 0, "pocion_salud": 0, "armadura": 0}
        self.inventory_open = False
        self.room_floor_items = {} # habitacion_num -> list[dict]

        # Inicialización del Patrón Command para registrar acciones del jugador
        self.command_map = {
            "space": AtacarComando(self),
            "h": UsarPocionComando(self),
            "u": UsarPocionComando(self),
            "e": InteractuarComando(self)
        }

        self._patch_bicho_sleep()

        self.root.bind("<KeyPress>",   self._on_key_down)
        self.root.bind("<KeyRelease>", self._on_key_up)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._cargar_juego()
        self._game_loop()

    # ── Parcheo en tiempo real del sueño de los hilos de los bichos ──
    def _patch_bicho_sleep(self):
        from Laberinto26.Entidades.Perezoso import Perezoso
        from Laberinto26.Entidades.Agresivo import Agresivo
        from Laberinto26.Entidades.Modo import Modo_Clase
        
        orig_perezoso_duerme = Perezoso.duerme
        orig_agresivo_duerme = Agresivo.duerme
        
        def new_perezoso_duerme(self_obj, un_bicho):
            un_bicho.is_sleeping = True
            orig_perezoso_duerme(self_obj, un_bicho)
            un_bicho.is_sleeping = False
            
        def new_agresivo_duerme(self_obj, un_bicho):
            un_bicho.is_sleeping = True
            orig_agresivo_duerme(self_obj, un_bicho)
            un_bicho.is_sleeping = False

        def new_camina(self_obj, un_bicho):
            # Los bichos NO caminan a nivel lógico por las puertas para quedarse en sus respectivas habitaciones
            pass
            
        Perezoso.duerme = new_perezoso_duerme
        Agresivo.duerme = new_agresivo_duerme
        Modo_Clase.camina = new_camina

    def _cargar_juego(self):
        ruta_oficial = r"C:\Uni\3º ESIIAB\2º cuatri\Diseño\Prácticas\1ºEntrega\Python\Mapa\Laberinto Del Olimpo.json"
        ruta_local   = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'Mapa',
            'Laberinto Del Olimpo.json'))

        vista = VistaLaberinto_Clase()
        for ruta in (ruta_oficial, ruta_local):
            try:
                self.juego = vista.crear_juego_desde_json(ruta)
                break
            except FileNotFoundError:
                continue

        if not self.juego:
            from Laberinto26.Juego import Juego_Clase
            self.juego = Juego_Clase()
            self.juego.crear_laberinto_4_habitacionesFM()

        self.juego.agregar_personaje("Hollow Knight")
        self.prota = self.juego.personaje

        # Forzar inicio en habitación 1
        hab1 = next((h for h in self.juego.laberinto.hijos if h.num == 1), None)
        if hab1:
            self.prota.posicion = hab1
        self.hab_actual = self.prota.posicion

        # Centrar jugador en la habitación de inicio
        self.player.x = ROOM_X + ROOM_W // 2
        self.player.y = ROOM_Y + ROOM_H // 2

        # Abrir todas las puertas del juego de momento (Comentado para poder usar llaves en puertas cerradas)
        # self.juego.abrir_todas_las_puertas()

        # Inicializar items del suelo para la habitación inicial si no existen
        if self.hab_actual:
            self.room_floor_items[self.hab_actual.num] = []
            if random.random() < 0.30:
                posibles = ["pocion", "llave", "espada"]
                tipo_item = random.choice(posibles)
                ix = random.randint(ROOM_X + TILE + 80, ROOM_X + ROOM_W - TILE - 80)
                iy = random.randint(ROOM_Y + TILE + 80, ROOM_Y + ROOM_H - TILE - 80)
                self.room_floor_items[self.hab_actual.num].append({
                    "x": ix, "y": iy, "tipo": tipo_item
                })



        self.juego.lanzar_todos_los_bichos()
        self._sincronizar_monstruos_tiempo_real()

    # ── Sincronizador de Monstruos en Tiempo Real (Aparecen/desaparecen al moverse) ──
    def _sincronizar_monstruos_tiempo_real(self):
        bichos_activos = [b for b in self.juego.bichos if getattr(b, 'posicion', None) == self.hab_actual and b.estaVivo()]
        
        # 1. Eliminar visualmente los que se han ido de la sala o han muerto
        for m in list(self.monsters):
            if m.bicho not in bichos_activos:
                # Si salió de la sala, crear efecto de desvanecimiento
                if m.bicho.estaVivo():
                    for _ in range(8):
                        self.particles.append(Particle(
                            m.x, m.y, random.uniform(-2, 2), random.uniform(-2, 2),
                            "#555577", random.randint(2, 4), 30
                        ))
                self.monsters.remove(m)

        # 2. Agregar visualmente los que acaban de entrar en la sala
        bichos_renderizados = [m.bicho for m in self.monsters]
        for b in bichos_activos:
            if b not in bichos_renderizados:
                is_guardian = getattr(b, 'esGuardian', lambda: False)()
                new_ai = MonsterAI(b, b.esAgresivo(), is_guardian=is_guardian)
                # Crear efecto de entrada (portal/humo)
                particle_color = "#ff6600" if is_guardian else "#555577"
                particle_count = 30 if is_guardian else 8
                for _ in range(particle_count):
                    self.particles.append(Particle(
                        new_ai.x, new_ai.y, random.uniform(-4, 4), random.uniform(-4, 4),
                        particle_color, random.randint(2, 5), 40
                    ))
                if is_guardian:
                    self.floating_texts.append(FloatingText(
                        new_ai.x, new_ai.y - 100, "⚔ EL GUARDIÁN DEL LABERINTO ⚔", "#ff6600", ("Consolas", 18, "bold")
                    ))
                    self.screen_shake = 30
                self.monsters.append(new_ai)

    def _on_key_down(self, event):
        key = event.keysym.lower()
        if key == "i" and self.prota and self.prota.estaVivo():
            self.inventory_open = not self.inventory_open
        elif key in self.command_map and self.prota and self.prota.estaVivo():
            self.command_map[key].ejecutar()
        else:
            if not self.inventory_open:
                self.player.key_down(event.keysym)

    def _on_key_up(self, event):
        self.player.key_up(event.keysym)

    def _on_close(self):
        self.running = False
        if self.juego:
            self.juego.terminar_todos_los_bichos()
        self.root.destroy()

    def _realizar_ataque(self):
        if self.player.attack_cooldown > 0:
            return

        self.player.attack_timer = 10
        self.player.attack_cooldown = 18

        px, py = self.player.x, self.player.y
        facing = self.player.facing
        
        # Lógica de la Espada del Olimpo: Niveles 1 a 5
        lvl = self.inventario["espada_olimpo"]
        base_dmg = getattr(self.prota, 'poder', 10)
        
        if lvl > 0:
            dmg = 25 if lvl == 5 else (15 + (lvl - 1) * 2)
            hit_range = int(95 * 1.5)
        else:
            dmg = base_dmg
            hit_range = 95

        spark_angles = {'N': -90, 'S': 90, 'E': 0, 'O': 180}
        base_angle = math.radians(spark_angles.get(facing, 0))
        
        if lvl == 5:
            spark_color = "#20df40"  # Chispas verde veneno tóxico para nivel 5
        elif lvl > 0:
            spark_color = "#ffd700"  # Chispas doradas para niveles 1-4
        else:
            spark_color = "#aaddff"  # Chispas originales
        for _ in range(8):
            ang = base_angle + random.uniform(-0.6, 0.6)
            spd = random.uniform(3, 6)
            self.particles.append(Particle(
                px + math.cos(base_angle)*30, py + math.sin(base_angle)*30,
                math.cos(ang)*spd, math.sin(ang)*spd,
                spark_color, random.randint(2, 4), 25
            ))

        for m in list(self.monsters):
            dx = m.x - px
            dy = m.y - py
            dist = math.hypot(dx, dy)

            if dist <= hit_range:
                aligned = False
                if facing == 'E' and dx >= -30: aligned = True
                elif facing == 'O' and dx <= 30: aligned = True
                elif facing == 'N' and dy <= 30: aligned = True
                elif facing == 'S' and dy >= -30: aligned = True
                if aligned:
                    m.bicho.vidas = max(0, m.bicho.vidas - dmg)
                    
                    # Si la espada es Nivel 5, infligir veneno: 5 de daño de veneno por 2 segundos
                    if lvl == 5:
                        m.poison_ticks_left = 2
                        m.last_poison_tick_time = time.time()
                        self.floating_texts.append(FloatingText(
                            m.x, m.y - 45, "🧪 ¡ENVENENADO!", "#20df40", ("Consolas", 10, "bold")
                        ))
                    
                    ang_hit = math.atan2(dy, dx)
                    m.x += math.cos(ang_hit) * 35
                    m.y += math.sin(ang_hit) * 35
                    
                    m_size = MONSTER_SIZE_AGR if m.is_agresivo else MONSTER_SIZE_PER
                    m.x = max(ROOM_X + TILE + m_size//4, min(ROOM_X + ROOM_W - TILE - m_size//4, m.x))
                    m.y = max(ROOM_Y + TILE + m_size//4, min(ROOM_Y + ROOM_H - TILE - m_size//4, m.y))

                    for _ in range(10):
                        self.particles.append(Particle(
                            m.x, m.y,
                            random.uniform(-4, 4), random.uniform(-4, 4),
                            "#ffffff", random.randint(2, 4), 20
                        ))

                    self.floating_texts.append(FloatingText(
                        m.x, m.y - 20, f"-{dmg}", "#00ffcc", ("Consolas", 14, "bold")
                    ))
                    
                    self.screen_shake = 6

                    if m.bicho.vidas == 0:
                        m.bicho.vidas = 0
                        self.juego.eliminar_bicho(m.bicho)
                        self.monsters.remove(m)
                        
                        self.floating_texts.append(FloatingText(
                            m.x, m.y - 40, "¡MUERTO! ☠", "#ff3333", ("Consolas", 15, "bold")
                        ))
                        
                        for _ in range(25):
                            self.particles.append(Particle(
                                m.x, m.y,
                                random.uniform(-5, 5), random.uniform(-5, 5),
                                "#3b1e54", random.randint(3, 6), 40
                            ))
                        
                        # ── Dropeo al matar un bicho agresivo ──
                        if m.is_agresivo:
                            if self.hab_actual.num not in self.room_floor_items:
                                self.room_floor_items[self.hab_actual.num] = []
                                
                            if random.random() < 0.30:
                                # Dropear pocima de salud
                                self.room_floor_items[self.hab_actual.num].append({
                                    "x": m.x, "y": m.y, "tipo": "pocion"
                                })
                                self.floating_texts.append(FloatingText(
                                    m.x, m.y - 65, "🧪 ¡Poción!", "#ff3333", ("Consolas", 11, "bold")
                                ))
                            if random.random() < 0.30:
                                # Dropear llave
                                self.room_floor_items[self.hab_actual.num].append({
                                    "x": m.x, "y": m.y, "tipo": "llave"
                                })
                                self.floating_texts.append(FloatingText(
                                    m.x, m.y - 85, "🔑 ¡Llave!", "#ffd700", ("Consolas", 11, "bold")
                                ))

    def _cambiar_habitacion(self, dir_name: str):
        dir_map = {"N": Norte(), "S": Sur(), "E": Este(), "O": Oeste()}

        dir_obj = dir_map[dir_name]
        puerta  = self.hab_actual.obtener_elemento(dir_obj)
        if not puerta:
            return

        destino = None
        if hasattr(puerta, 'lado1') and puerta.lado1 != self.hab_actual:
            destino = puerta.lado1
        elif hasattr(puerta, 'lado2') and puerta.lado2 != self.hab_actual:
            destino = puerta.lado2
        if destino is None:
            return

        # Cambio instantáneo de habitación
        self.hab_actual = destino
        self.prota.posicion = destino
        self._sincronizar_monstruos_tiempo_real()

        cx = ROOM_X + ROOM_W // 2
        cy = ROOM_Y + ROOM_H // 2

        # ── Nuevas Reglas Matemáticas de Posicionamiento según la Dirección ──
        if dir_name == "N":
            # Cruza al NORTE -> Aparece en el SUR de la nueva sala
            # Posición X alineada con el centro de la puerta, Y es: Posición_Puerta_Y - (Tamaño_Bloque * 2)
            self.player.x = cx
            self.player.y = (ROOM_Y + ROOM_H - TILE) - (TILE * 2)
        elif dir_name == "S":
            # Cruza al SUR -> Aparece en el NORTE de la nueva sala
            # Posición X alineada con el centro, Y es: Posición_Puerta_Y + (Tamaño_Bloque * 2)
            self.player.x = cx
            self.player.y = (ROOM_Y + TILE) + (TILE * 2)
        elif dir_name == "E":
            # Cruza al ESTE -> Aparece en el OESTE de la nueva sala
            # Posición Y alineada con el centro, X es: Posición_Puerta_X + (Tamaño_Bloque * 2)
            self.player.x = (ROOM_X + TILE) + (TILE * 2)
            self.player.y = cy
        elif dir_name == "O":
            # Cruza al OESTE -> Aparece en el ESTE de la nueva sala
            # Posición Y alineada con el centro, X es: Posición_Puerta_X - (Tamaño_Bloque * 2)
            self.player.x = (ROOM_X + ROOM_W - TILE) - (TILE * 2)
            self.player.y = cy

        self.transition_cooldown = 35

        # Rol de 30% de encontrar la espada, la llave o la poción al entrar en una sala por primera vez
        if destino.num not in self.room_floor_items:
            self.room_floor_items[destino.num] = []
            if random.random() < 0.30:
                posibles = ["pocion", "llave"]
                if self.inventario["espada_olimpo"] < 5:
                    posibles.append("espada")
                tipo_item = random.choice(posibles)
                ix = random.randint(ROOM_X + TILE + 80, ROOM_X + ROOM_W - TILE - 80)
                iy = random.randint(ROOM_Y + TILE + 80, ROOM_Y + ROOM_H - TILE - 80)
                self.room_floor_items[destino.num].append({
                    "x": ix, "y": iy, "tipo": tipo_item
                })

    def _game_loop(self):
        if not self.running:
            return

        self.anim_tick += 1

        # 🏆 PANTALLA GIGANTE DE VICTORIA (HABITACIÓN 14 ES EL FINAL) 🏆
        if self.hab_actual and self.hab_actual.num == 14:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, WIN_W, WIN_H, fill="#04020a", outline="")
            
            # Dibujar un efecto de partículas mágicas o estrellas en movimiento
            for i in range(50):
                random.seed(i * 99)
                sx_ = random.randint(20, WIN_W - 20)
                sy_ = random.randint(20, WIN_H - 20)
                size_ = random.choice([2, 3, 4])
                opacity_ = random.choice(["#3a2c5e", "#5c3d91", "#ffd700", "#00ffff"])
                self.canvas.create_oval(sx_, sy_, sx_ + size_, sy_ + size_, fill=opacity_, outline="")
            
            # Texto "gracias por jugar" en grande
            self.canvas.create_text(WIN_W // 2, WIN_H // 2 - 40,
                                    text="¡GRACIAS POR JUGAR!",
                                    fill="#c08500", font=("Consolas", 36, "bold"))
            self.canvas.create_text(WIN_W // 2 - 2, WIN_H // 2 - 42,
                                    text="¡GRACIAS POR JUGAR!",
                                    fill="#ffd700", font=("Consolas", 36, "bold"))
            
            # Subtítulo de felicitaciones
            self.canvas.create_text(WIN_W // 2, WIN_H // 2 + 30,
                                    text="Has superado los peligros del Laberinto 26 y completado tu misión.",
                                    fill="#a899c3", font=("Consolas", 14, "italic"))
            
            # Realizado por Billy abajo en pequeño
            self.canvas.create_text(WIN_W // 2, WIN_H - 60,
                                    text="realizado por Billy",
                                    fill="#5a4d75", font=("Consolas", 10, "bold"))
            
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)
            self.root.after(16, self._game_loop)
            return

        # Sincronizar bichos en tiempo real
        if self.prota and self.prota.estaVivo() and not self.inventory_open:
            self._sincronizar_monstruos_tiempo_real()

        # ── 1. ACTUALIZAR POSICIÓN JUGADOR ──
        if self.prota and self.prota.estaVivo() and not self.inventory_open:
            self.player.update()

            if self.transition_cooldown > 0:
                self.transition_cooldown -= 1
            else:
                dir_trans = self.player.check_door_transition(self.hab_actual, self)
                if dir_trans:
                    self._cambiar_habitacion(dir_trans)

            # ── 1.1 Colisiones con Items en el Suelo ──
            items = self.room_floor_items.get(self.hab_actual.num, [])
            for item in list(items):
                dist = math.hypot(self.player.x - item["x"], self.player.y - item["y"])
                if dist < 26:
                    tipo = item["tipo"]
                    
                    if tipo == "llave":
                        from Laberinto26.ElementosFisicos.Llave import Llave
                        obj = Llave()
                        obj.entrar(self.prota)
                        self.inventario["llave"] += 1
                        txt = "+1 Llave 🔑"
                        color = "#ffd700"
                    elif tipo == "espada":
                        from Laberinto26.ElementosFisicos.EspadaOlimpo import EspadaOlimpo
                        obj = EspadaOlimpo()
                        obj.entrar(self.prota)
                        
                        # Lógica de subida de nivel (máximo 5)
                        lvl = self.inventario.get("espada_olimpo", 0)
                        if lvl < 5:
                            self.inventario["espada_olimpo"] = lvl + 1
                            new_lvl = lvl + 1
                            if new_lvl == 5:
                                txt = "¡Espada del Olimpo MÁXIMA! (Lvl 5) 🗡️⚡"
                            else:
                                txt = f"¡Espada del Olimpo Lvl {new_lvl}! 🗡️✨"
                        else:
                            txt = "Espada del Olimpo Lvl 5 (Máx) 🗡️✨"
                        color = "#00ffff"
                    elif tipo == "pocion":
                        from Laberinto26.ElementosFisicos.PocionSalud import PocionSalud
                        obj = PocionSalud()
                        obj.entrar(self.prota)
                        self.inventario["pocion_salud"] += 1
                        txt = "+1 Poción de Salud 🧪"
                        color = "#ff3333"
                    elif tipo == "armadura":
                        # Aumento de nivel de la Armadura Misterio del Laberinto (hasta Nivel 3)
                        lvl = self.inventario.get("armadura", 0)
                        if lvl < 3:
                            self.inventario["armadura"] = lvl + 1
                            new_lvl = lvl + 1
                            new_max = 50 + new_lvl * 25
                            self.prota.vidas = new_max  # Curación instantánea completa
                            txt = f"¡Armadura Misterio Lvl {new_lvl}! 🛡️💜"
                            
                            self.floating_texts.append(FloatingText(
                                self.player.x, self.player.y - 50, f"Salud Máx: {new_max} ❤️", "#ff33aa", ("Consolas", 12, "bold")
                            ))
                        else:
                            txt = "Armadura Misterio Lvl 3 (Máx) 🛡️💜"
                        color = "#b92bcf"
                    
                    self.floating_texts.append(FloatingText(
                        item["x"], item["y"] - 30, txt, color, ("Consolas", 14, "bold")
                    ))
                    
                    for _ in range(15):
                        self.particles.append(Particle(
                            item["x"], item["y"], random.uniform(-3, 3), random.uniform(-3, 3),
                            color, random.randint(2, 4), 25
                        ))
                    
                    items.remove(item)

            # ── Detección de Bombas en Suelo ──
            bombas = [h for h in self.hab_actual.hijos if getattr(h, 'EsBomba', lambda: False)()]
            for bomba in bombas:
                bx = getattr(bomba, 'x', None)
                by = getattr(bomba, 'y', None)
                if bx is not None and by is not None:
                    dist_bomba = math.hypot(self.player.x - bx, self.player.y - by)
                    if dist_bomba < 24:
                        # Identificador único de bomba por habitación y posición
                        bomba_id = f"{self.hab_actual.num}_{bx}_{by}"
                        if bomba_id not in self.triggered_bombs:
                            self.triggered_bombs.add(bomba_id)
                            
                            if getattr(bomba, 'activa', True):
                                if getattr(bomba, 'EsBombaVeneno', lambda: False)():
                                    # 🧪 EXPLOSIÓN VENENOSA DoT: 5 daño/seg por 10 segundos
                                    self.player_poison_ticks = 10
                                    self.player_poison_last_tick = time.time()
                                    self.screen_shake = 22
                                    
                                    # Partículas de gas tóxico verde
                                    for _ in range(40):
                                        self.particles.append(Particle(
                                            bx, by, random.uniform(-6, 6), random.uniform(-6, 6),
                                            random.choice(["#20df40", "#32cd32", "#00ff00", "#105010"]),
                                            random.randint(3, 7), 35
                                        ))
                                    self.floating_texts.append(FloatingText(
                                        bx, by - 30, "¡¡ GAS TÓXICO !! 🧪💥", "#20df40", ("Consolas", 15, "bold")
                                    ))
                                    self.floating_texts.append(FloatingText(
                                        self.player.x, self.player.y - 50, "-5 HP/s (Veneno)", "#20df40", ("Consolas", 12, "bold")
                                    ))
                                    bomba.activa = False
                                else:
                                    # 💣 EXPLOSIÓN ACTIVA
                                    bomba.entrar(self.prota) # Llama a la lógica oficial del dominio
                                    self.screen_shake = 24
                                    
                                    # Efectos de explosión de fuego y humo
                                    for _ in range(40):
                                        self.particles.append(Particle(
                                            bx, by, random.uniform(-7, 7), random.uniform(-7, 7),
                                            random.choice(["#ff3300", "#ffaa00", "#555555"]),
                                            random.randint(3, 7), 35
                                        ))
                                    
                                    self.floating_texts.append(FloatingText(
                                        bx, by - 30, "¡¡ PUUUM !! 💥", "#ff3300", ("Consolas", 18, "bold")
                                    ))
                                    self.floating_texts.append(FloatingText(
                                        self.player.x, self.player.y - 50, "-15 HP", "#ff0000", ("Consolas", 16, "bold")
                                    ))
                                    bomba.activa = False # Queda inactiva después de estallar
                            else:
                                # 🍀 BOMBA DESACTIVADA
                                self.floating_texts.append(FloatingText(
                                    self.player.x, self.player.y - 30, "Esta desactivada, ¡qué suerte! 🍀", "#20df40", ("Consolas", 12, "bold")
                                ))
                                for _ in range(10):
                                    self.particles.append(Particle(
                                        self.player.x, self.player.y, random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5),
                                        "#20df40", random.randint(2, 3), 20
                                    ))

        # ── 2. ACTUALIZAR ENEMIGOS Y DAÑOS ──
        if not self.inventory_open:
            now = time.time()
            for m in list(self.monsters):
                # --- Aplicar Daño de Veneno (Nivel 5) ---
                if getattr(m, 'poison_ticks_left', 0) > 0:
                    if now - getattr(m, 'last_poison_tick_time', 0.0) >= 1.0:
                        m.poison_ticks_left -= 1
                        m.last_poison_tick_time = now
                        
                        m.bicho.vidas = max(0, m.bicho.vidas - 5)
                        
                        # Texto flotante verde
                        self.floating_texts.append(FloatingText(
                            m.x, m.y - 30, "-5 Veneno 🧪", "#20df40", ("Consolas", 12, "bold")
                        ))
                        
                        # Partículas verdes de veneno
                        for _ in range(12):
                            self.particles.append(Particle(
                                m.x, m.y, random.uniform(-3, 3), random.uniform(-3, 3),
                                "#20df40", random.randint(2, 4), 25
                            ))
                        
                        # Muerte por veneno
                        if m.bicho.vidas == 0:
                            self.juego.eliminar_bicho(m.bicho)
                            if m in self.monsters:
                                self.monsters.remove(m)
                            
                            self.floating_texts.append(FloatingText(
                                m.x, m.y - 40, "¡MUERTO! ☠", "#ff3333", ("Consolas", 15, "bold")
                            ))
                            
                            for _ in range(25):
                                self.particles.append(Particle(
                                    m.x, m.y, random.uniform(-5, 5), random.uniform(-5, 5),
                                    "#3b1e54", random.randint(3, 6), 40
                                ))
                            
                            # Dropeos del monstruo
                            if m.is_agresivo or m.is_guardian:
                                if self.hab_actual.num not in self.room_floor_items:
                                    self.room_floor_items[self.hab_actual.num] = []
                                if random.random() < 0.30:
                                    self.room_floor_items[self.hab_actual.num].append({"x": m.x, "y": m.y, "tipo": "pocion"})
                                if random.random() < 0.30:
                                    self.room_floor_items[self.hab_actual.num].append({"x": m.x, "y": m.y, "tipo": "llave"})
                                # El Guardián siempre dropea una espada
                                if m.is_guardian:
                                    self.room_floor_items[self.hab_actual.num].append({"x": m.x + 20, "y": m.y, "tipo": "espada"})
                                    self.room_floor_items[self.hab_actual.num].append({"x": m.x - 20, "y": m.y, "tipo": "pocion"})
                                    self.floating_texts.append(FloatingText(
                                        m.x, m.y - 80, "¡¡GUARDIÁN DERROTADO!!", "#ffd700", ("Consolas", 20, "bold")
                                    ))
                                    self.screen_shake = 40
                            continue

                # Continuar actualización normal del bicho
                m.update(self.player.x, self.player.y)
                
                is_sleeping = getattr(m.bicho, 'is_sleeping', False)
                if is_sleeping and self.anim_tick % 45 == 0:
                    text_z = "Zz!" if m.is_agresivo else "Zzz..."
                    color_z = "#ff4444" if m.is_agresivo else "#55aaff"
                    self.floating_texts.append(FloatingText(
                        m.x + (15 if m.is_agresivo else 5), m.y - (30 if m.is_agresivo else 15),
                        text_z, color_z, ("Consolas", 10, "italic" if not m.is_agresivo else "bold")
                    ))
                
                dist = math.hypot(m.x - self.player.x, m.y - self.player.y)
                if m.is_guardian:
                    m_size = GUARDIAN_SIZE
                elif m.is_agresivo:
                    m_size = MONSTER_SIZE_AGR
                else:
                    m_size = MONSTER_SIZE_PER
                limit = (PLAYER_SIZE + m_size) // 2 - 12
                
                if dist < limit and self.prota and self.prota.estaVivo():
                    cooldown = 2.0 if m.is_guardian else (3.0 if m.is_agresivo else 5.0)
                    
                    if now - m.last_hit_time >= cooldown:
                        m.last_hit_time = now
                        
                        dmg = 25 if m.is_guardian else getattr(m.bicho, 'poder', 10)
                        self.prota.vidas = max(0, self.prota.vidas - dmg)
                        
                        self.screen_shake = 12
                        color_txt = "#ff3333" if m.is_agresivo else "#ff7733"
                        self.floating_texts.append(FloatingText(
                            self.player.x, self.player.y - 30, f"-{dmg} HP", color_txt, ("Consolas", 16, "bold")
                        ))
                        
                        for _ in range(12):
                            self.particles.append(Particle(
                                self.player.x, self.player.y,
                                random.uniform(-4, 4), random.uniform(-4, 4),
                                "#ff2200", random.randint(2, 5), 30
                            ))

        # ── 2.5 COLISIÓN BOMBAS DEL GUARDIÁN ──
        if self.prota and self.prota.estaVivo():
            now = time.time()
            for m in self.monsters:
                if m.is_guardian:
                    for bomb in list(m.bombs):
                        if bomb.exploded:
                            m.bombs.remove(bomb)
                            continue
                        # Colisión bomba con jugador
                        dist = math.hypot(bomb.x - self.player.x, bomb.y - self.player.y)
                        if dist < 30:
                            bomb.exploded = True
                            # Explosión naranja
                            self.screen_shake = 15
                            for _ in range(20):
                                self.particles.append(Particle(
                                    bomb.x, bomb.y, random.uniform(-6, 6), random.uniform(-6, 6),
                                    random.choice(["#ff6600", "#ffaa00", "#ff3300"]),
                                    random.randint(3, 6), 30
                                ))
                            self.floating_texts.append(FloatingText(
                                bomb.x, bomb.y - 20, "¡BOMBA! 💥", "#ff6600", ("Consolas", 14, "bold")
                            ))
                            # Aplicar quemadura DoT: 5 daño/seg por 5 segundos
                            self.player_burn_ticks = 5
                            self.player_burn_last_tick = now

            # Aplicar daño de quemadura continua
            if self.player_burn_ticks > 0:
                if now - self.player_burn_last_tick >= 1.0:
                    self.player_burn_last_tick = now
                    self.player_burn_ticks -= 1
                    self.prota.vidas = max(0, self.prota.vidas - 5)
                    self.floating_texts.append(FloatingText(
                        self.player.x, self.player.y - 40, "-5 🔥 Quemadura", "#ff6600", ("Consolas", 12, "bold")
                    ))
                    for _ in range(8):
                        self.particles.append(Particle(
                            self.player.x + random.randint(-15, 15),
                            self.player.y + random.randint(-15, 15),
                            random.uniform(-1, 1), random.uniform(-2, 0),
                            "#ff6600", random.randint(2, 3), 20
                        ))

            # Aplicar daño de veneno continuo (5 de daño por segundo por 10 segundos)
            if self.player_poison_ticks > 0:
                if now - self.player_poison_last_tick >= 1.0:
                    self.player_poison_last_tick = now
                    self.player_poison_ticks -= 1
                    self.prota.vidas = max(0, self.prota.vidas - 5)
                    self.floating_texts.append(FloatingText(
                        self.player.x, self.player.y - 40, "-5 🧪 Veneno", "#20df40", ("Consolas", 12, "bold")
                    ))
                    for _ in range(12):
                        self.particles.append(Particle(
                            self.player.x + random.randint(-15, 15),
                            self.player.y + random.randint(-15, 15),
                            random.uniform(-1.5, 1.5), random.uniform(-2, 0),
                            "#20df40", random.randint(2, 3), 22
                        ))

        # ── 3. ACTUALIZAR EFECTOS VISUALES ──
        for ft in list(self.floating_texts):
            ft.update()
            if ft.life <= 0:
                self.floating_texts.remove(ft)

        for p in list(self.particles):
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        dx, dy = 0, 0
        if self.screen_shake > 0:
            dx = random.randint(-self.screen_shake, self.screen_shake)
            dy = random.randint(-self.screen_shake, self.screen_shake)
            self.screen_shake -= 1

        # ── 4. RENDERIZACIÓN GRÁFICA COMPLETA ──
        self.canvas.delete("all")

        self.renderer.draw_background()

        if self.hab_actual:
            self.renderer.draw_room(self.hab_actual, floor_items=self.room_floor_items.get(self.hab_actual.num, []))

        # Partículas
        for p in self.particles:
            p.draw(self.canvas)

        # Renderizado de Enemigos
        for m in self.monsters:
            if m.is_guardian:
                kind = "guardian"
                label = f"GUARDIÁN ({m.bicho.vidas} HP)"
                bob = math.sin(self.anim_tick * 0.04) * 6
                self.renderer.draw_entity(int(m.x), int(m.y), kind,
                                          m.bicho.vidas, m.bicho.nombre,
                                          max_vidas=250, label=label, bobbing=bob)
                # Dibujar bombas del guardián
                for bomb in m.bombs:
                    if not bomb.exploded:
                        bomb.draw(self.canvas)
                # Boss health bar grande en la parte superior de la pantalla
                boss_bar_w = 400
                boss_bar_h = 12
                boss_bar_x = ROOM_X + (ROOM_W - boss_bar_w) // 2
                boss_bar_y = 20
                boss_pct = max(0.0, m.bicho.vidas / 250)
                self.canvas.create_rectangle(boss_bar_x - 1, boss_bar_y - 1,
                                             boss_bar_x + boss_bar_w + 1, boss_bar_y + boss_bar_h + 1,
                                             fill="", outline="#ff6600", width=1)
                self.canvas.create_rectangle(boss_bar_x, boss_bar_y,
                                             boss_bar_x + boss_bar_w, boss_bar_y + boss_bar_h,
                                             fill="#0a0e18", outline="")
                fill_w = int(boss_bar_w * boss_pct)
                if fill_w > 0:
                    self.canvas.create_rectangle(boss_bar_x, boss_bar_y,
                                                 boss_bar_x + fill_w, boss_bar_y + boss_bar_h,
                                                 fill="#ff6600", outline="")
                self.canvas.create_text(boss_bar_x + boss_bar_w // 2, boss_bar_y + boss_bar_h // 2,
                                        text=f"EL GUARDIÁN DEL LABERINTO — {m.bicho.vidas}/250",
                                        fill="#ffffff", font=("Consolas", 8, "bold"))
            else:
                kind = "agresivo" if m.is_agresivo else "perezoso"
                label = f"Mazo ({m.bicho.vidas} HP)" if m.is_agresivo else f"Escarabajo ({m.bicho.vidas} HP)"
                
                is_sleeping = getattr(m.bicho, 'is_sleeping', False)
                bob = 0 if is_sleeping else (math.sin(self.anim_tick * 0.1) * 3 if m.is_agresivo else math.cos(self.anim_tick * 0.05) * 2)
                
                self.renderer.draw_entity(int(m.x), int(m.y), kind,
                                          m.bicho.vidas, m.bicho.nombre,
                                          label=label, bobbing=bob, sleeping=is_sleeping)

        # Renderizado del Jugador (Hollow Knight) - SOLO SI SIGUE VIVO
        if self.prota and self.prota.estaVivo():
            walking_bob = 0
            if self.player.vx != 0 or self.player.vy != 0:
                walking_bob = abs(math.sin(self.anim_tick * 0.25)) * -5
            
            player_max_hp = 50 + self.inventario["armadura"] * 25
            self.renderer.draw_entity(int(self.player.x), int(self.player.y),
                                      "prota", self.prota.vidas,
                                      self.prota.nombre, max_vidas=player_max_hp,
                                      bobbing=walking_bob)

        # Renderizado de Espadazo (Si está atacando)
        if self.player.attack_timer > 0 and self.prota and self.prota.estaVivo():
            self.renderer.draw_attack_slash(
                int(self.player.x), int(self.player.y),
                self.player.facing, self.player.attack_timer,
                espada_level=self.inventario["espada_olimpo"]
            )

        # Prompt interactivo para Armarios cercanos
        if self.hab_actual and self.prota and self.prota.estaVivo():
            armarios = [h for h in self.hab_actual.hijos if h.__class__.__name__ == 'Armario_Clase']
            for arm in armarios:
                if not getattr(arm, 'abierto', False):
                    dist = math.hypot(self.player.x - arm.x, self.player.y - arm.y)
                    if dist <= 50:
                        # Dibujar prompt brillante e interactivo
                        self.canvas.create_rectangle(arm.x - 70, arm.y + 26, arm.x + 70, arm.y + 44,
                                                     fill="#0d0d0d", outline="#ffd700", width=1.5)
                        self.canvas.create_text(arm.x, arm.y + 35, text="[E] Abrir Armario 🚪",
                                                fill="#ffffff", font=("Consolas", 9, "bold"))

        # Textos flotantes
        for ft in self.floating_texts:
            ft.draw(self.canvas)

        # Panel Lateral Hollow Knight HUD y Mini-Mapa
        all_rooms = self.juego.laberinto.hijos if self.juego and self.juego.laberinto else []
        self.renderer.draw_sidebar(self.prota, self.hab_actual, all_rooms, inventario=self.inventario)

        # ── PANTALLA DE INVENTARIO HUD (Presionando I) ──
        if self.inventory_open and self.prota and self.prota.estaVivo():
            # Fondo semi-transparente oscuro SOLO en la zona de juego (mantiene HUD y Mapa brillantes a la derecha)
            self.canvas.create_rectangle(0, 0, 840, WIN_H, fill="#04020a", stipple="gray50")
            
            # Marco del inventario (centrado a la izquierda del HUD lateral)
            ix, iy, iw, ih = 170, 90, 500, 420
            self.canvas.create_rectangle(ix, iy, ix + iw, iy + ih, fill="#0c071b", outline="#6a0dad", width=4)
            self.canvas.create_rectangle(ix + 10, iy + 10, ix + iw - 10, iy + ih - 10, fill="#06030e", outline="#3c146e", width=2)
            
            # Título principal
            self.canvas.create_text(ix + iw//2, iy + 35, text="INVENTARIO DE HOLLOW KNIGHT", fill="#ffd700", font=("Consolas", 18, "bold"))
            self.canvas.create_line(ix + 40, iy + 55, ix + iw - 40, iy + 55, fill="#6a0dad", width=2)
            
            # --- Fila 1: Llave ---
            ly = iy + 85
            self.canvas.create_text(ix + 50, ly, anchor="w", text="🔑 Llave de Mazmorra", fill="#ffd700", font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 450, ly, anchor="e", text=f"Cant: {self.inventario['llave']}", fill="#ffffff", font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 50, ly + 22, anchor="w", text="Abre cualquier puerta cerrada automáticamente al cruzarla.", fill="#8888aa", font=("Consolas", 9, "italic"))
            self.canvas.create_line(ix + 30, ly + 40, ix + iw - 30, ly + 40, fill="#1c0f2a", width=1)
            
            # --- Fila 2: Poción ---
            py_ = iy + 155
            self.canvas.create_text(ix + 50, py_, anchor="w", text="🧪 Poción de Salud", fill="#ff5555", font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 450, py_, anchor="e", text=f"Cant: {self.inventario['pocion_salud']}", fill="#ffffff", font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 50, py_ + 22, anchor="w", text="Recupera la salud al 100%. Presiona [H] o [U] para usar.", fill="#8888aa", font=("Consolas", 9, "italic"))
            self.canvas.create_line(ix + 30, py_ + 40, ix + iw - 30, py_ + 40, fill="#1c0f2a", width=1)
            
            # --- Fila 3: Espada del Olimpo ---
            ey = iy + 225
            lvl = self.inventario["espada_olimpo"]
            if lvl == 5:
                sword_color = "#20df40"  # Verde veneno
                status_text = "LVL 5 (MÁX) 🧪⚡"
                desc_text = "Daño: 25 | Rango: +50% | Pasiva: Veneno (5 daño/seg por 2 seg)"
            elif lvl > 0:
                sword_color = "#00ffff"  # Celeste
                status_text = f"EQUIPADO: LVL {lvl} 🗡️"
                dmg = 15 + (lvl - 1) * 2
                desc_text = f"Daño: {dmg} KI | Rango: +50% | ¡Busca más espadas para subir de nivel!"
            else:
                sword_color = "#555555"  # Gris
                status_text = "NO POSEÍDO"
                desc_text = "Daño: 10 base. Encuéntrala en mazmorras o cofres."
                
            self.canvas.create_text(ix + 50, ey, anchor="w", text="🗡️ Espada del Olimpo", fill=sword_color, font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 450, ey, anchor="e", text=status_text, fill=sword_color, font=("Consolas", 12, "bold"))
            self.canvas.create_text(ix + 50, ey + 22, anchor="w", text=desc_text, fill="#8888aa", font=("Consolas", 9, "italic"))
            self.canvas.create_line(ix + 30, ey + 40, ix + iw - 30, ey + 40, fill="#1c0f2a", width=1)
            
            # --- Fila 4: Armadura Misterio ---
            ay = iy + 295
            alvl = self.inventario.get("armadura", 0)
            if alvl == 3:
                armor_color = "#b92bcf"  # Morado brillante
                armor_status = "LVL 3 (MÁX) 🛡️⚡"
                armor_desc = "Max HP: 125 (+150%) | La protección misteriosa definitiva de la mazmorra."
            elif alvl > 0:
                armor_color = "#a040d0"
                armor_status = f"EQUIPADO: LVL {alvl} 🛡️"
                hp_bonus = 50 + alvl * 25
                armor_desc = f"Max HP: {hp_bonus} (+{alvl * 50}%) | Encuentra armarios negros para mejorarla."
            else:
                armor_color = "#555555"
                armor_status = "NO POSEÍDO"
                armor_desc = "Max HP: 50 base. Explora armarios negros al lado de las paredes."
                
            self.canvas.create_text(ix + 50, ay, anchor="w", text="🛡️ Armadura Misterio", fill=armor_color, font=("Consolas", 14, "bold"))
            self.canvas.create_text(ix + 450, ay, anchor="e", text=armor_status, fill=armor_color, font=("Consolas", 12, "bold"))
            self.canvas.create_text(ix + 50, ay + 22, anchor="w", text=armor_desc, fill="#8888aa", font=("Consolas", 9, "italic"))
            self.canvas.create_line(ix + 30, ay + 40, ix + iw - 30, ay + 40, fill="#1c0f2a", width=1)
            
            # Pie de inventario
            self.canvas.create_text(ix + iw//2, iy + ih - 25, text="Presiona [I] para cerrar el inventario", fill="#ffd700", font=("Consolas", 11, "bold"))

        # 💀 PANTALLA GIGANTE Y SANGRIENTA DE MUERTE 💀
        if self.prota and not self.prota.estaVivo():
            # Fondo negro absoluto opaco que cubre toda la pantalla del juego
            self.canvas.create_rectangle(0, 0, WIN_W, WIN_H, fill="#020005", outline="")
            
            # Generar goteo de sangre sangrienta animada en la pantalla negra
            if self.anim_tick % 4 == 0:
                self.blood_drips.append({
                    'x': random.randint(100, WIN_W - 100),
                    'y': random.randint(-20, 100),
                    'length': random.randint(30, 200),
                    'speed': random.uniform(1.5, 4.0),
                    'width': random.randint(2, 5)
                })
                
            for drip in list(self.blood_drips):
                drip['y'] += drip['speed']
                # Dibujar rastro de sangre
                self.canvas.create_line(drip['x'], drip['y'], drip['x'], drip['y'] + drip['length'],
                                         fill="#8b0000", width=drip['width'])
                if drip['y'] > WIN_H:
                    self.blood_drips.remove(drip)
            
            # Texto "HAS MUERTO" Gigantesco, Gótico, Rojo y Sangriento en el centro
            # Efecto de sombra de sangre expandida detrás
            self.canvas.create_text(WIN_W // 2, WIN_H // 2 - 40,
                                    text="☠  HAS MUERTO  ☠",
                                    fill="#500000", font=("Consolas", 64, "bold"))
            self.canvas.create_text(WIN_W // 2 - 4, WIN_H // 2 - 44,
                                    text="☠  HAS MUERTO  ☠",
                                    fill="#ff0000", font=("Consolas", 64, "bold"))
            
            # Subtítulo descriptivo dramático
            self.canvas.create_text(WIN_W // 2, WIN_H // 2 + 50,
                                    text="Tu alma ha sido desintegrada y consumida por el laberinto.",
                                    fill="#7f6f75", font=("Consolas", 15, "italic"))
            self.canvas.create_text(WIN_W // 2, WIN_H // 2 + 100,
                                    text="Cierra la ventana para regresar al abismo.",
                                    fill="#4a4045", font=("Consolas", 12))

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.root.after(16, self._game_loop)

    def iniciar(self):
        self.root.mainloop()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    interfaz = MainInterfaz()
    interfaz.iniciar()
