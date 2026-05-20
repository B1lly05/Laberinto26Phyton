# 🎮 Laberinto26: Reingeniería y Patrones de Diseño (Pharo a Python)

¡Bienvenido a **Laberinto26**! Este proyecto representa una migración, refactorización y reingeniería completa de un sistema de laberinto interactivo originalmente diseñado en **Pharo (Smalltalk)** hacia **Python 3**. 

El objetivo principal es aplicar los principios de diseño de software **SOLID** y los patrones de diseño clásicos (**GoF**) para construir una arquitectura altamente modular, extensible y mantenible, acompañada de una **interfaz gráfica premium interactiva** inspirada en la estética oscura de *Hollow Knight* y las mecánicas de *The Binding of Isaac*.

---

## 📸 Características Destacadas

*   **Interfaz Gráfica Avanzada (Tkinter + PIL)**:
    *   **Estética Hollow Knight**: HUD elegante y minimalista con barras de vida estilizadas, menú lateral de inventario y renderizado con sombras realistas.
    *   **Animación de Transición de Salas**: Desplazamientos fluidos tipo *slide* (estilo *The Legend of Zelda* / *Isaac*) al cruzar puertas.
    *   **Efectos Visuales Activos**: Sistema de partículas dinámicas por colisiones, rastros de ataques de espada, textos flotantes de daño/curación y cráteres quemados para las bombas detonadas.
*   **Mecánicas de Juego Completas**:
    *   Movimiento libre del personaje con controles `WASD`.
    *   Sistema de combate en tiempo real con la **Espada del Olimpo** (`ESPACIO`).
    *   Inventario dinámico (`I`) y recolección de equipamiento (Pociones de salud, Llaves, Espadas y Armaduras de misterio con aumento de vida máxima).
    *   Enemigos inteligentes con diferentes comportamientos: **Agresivo** (persigue activamente), **Perezoso** (se desplaza aleatoriamente y duerme) y el **Boss Guardián** del Laberinto.
    *   Elementos destructivos y de almacenamiento: **Armarios con trampa de bomba de veneno**, **Paredes con bombas**, y pasadizos.

---

## 🛠️ Patrones de Diseño Implementados

La arquitectura del proyecto está construida de forma estricta sobre patrones de diseño de software para garantizar la modularidad y el bajo acoplamiento:

1.  **Composite (Estructural)**:
    *   Define una jerarquía uniforme de elementos físicos. La clase abstracta `ElementoMapa_Clase` es heredada por hojas (`Pared`, `Puerta`, `Bomba`) y contenedores (`Laberinto_Clase`, `Habitacion_Clase`), permitiendo tratarlos de forma homogénea.
2.  **Visitor (Comportamiento)**:
    *   Permite ejecutar operaciones globales (abrir/cerrar todas las puertas, activar/desactivar todas las trampas de bombas) recorriendo la estructura de árbol del laberinto sin violar la encapsulación. Utiliza la técnica de **Doble Despacho (Double Dispatch)** a través del método `aceptar(visitor)`.
3.  **Builder (Creacional)**:
    *   Ubicado en `Laberinto26_builder/`, este patrón desacopla el proceso de construcción compleja de un laberinto paso a paso (añadir habitaciones, colocar puertas orientadas, posicionar bombas) de su representación final.
4.  **Factory Method (Creacional)**:
    *   `Juego_Clase` actúa como el creador que define los métodos de fabricación de piezas (`fabricar_habitacion`, `fabricar_pared`, `fabricar_puerta`). Las subclases pueden alterar los componentes físicos creados sin modificar la lógica principal de ensamblado del juego.
5.  **Decorator (Estructural)**:
    *   Utilizado para añadir comportamiento dinámico a los elementos del mapa, como decorar paredes normales en `ParedBomba` o armarios estándar en `ArmarioBombaVeneno`.
6.  **State (Comportamiento)**:
    *   Gobierna el comportamiento dinámico de los enemigos (`Bicho`) según su modo actual de IA (`Agresivo`, `Perezoso`).

---

## 📁 Estructura del Directorio

```text
├── Laberinto.mdj              # Archivo de modelado de software en StarUML
├── diagramas_diseno.md        # Diagrama de Clases y Secuencia detallado (Mermaid)
├── README.md                  # El archivo que estás leyendo ahora
│
├── Laberinto26/               # Módulo Principal del Juego
│   ├── ElementosFisicos/      # Clases de la jerarquía Composite (Habitacion, Bomba, etc.)
│   ├── Entidades/             # Personaje, Boss, Bichos e Inteligencias Artificiales
│   ├── Visitor/               # Clases y derivaciones del Patrón Visitor
│   ├── Orientaciones/         # Clases de dirección cardinal (Norte, Sur, Este, Oeste)
│   ├── Estados/               # Estados y modos de comportamiento
│   ├── Comandos/              # Implementación de acciones del juego
│   ├── assets/                # Texturas, sprites de personajes y recursos visuales (.png)
│   ├── Juego.py               # Lógica del bucle y controladores centrales
│   ├── MainInterfaz.py        # Ventana del juego, renderizadores y controladores de teclado
│   └── Main.py                # Inicialización tradicional en consola
│
├── Laberinto26_builder/       # Implementación del Patrón Builder
│   ├── LaberintoBuilder.py
│   ├── Director.py
│   └── VistaLaberinto.py
│
└── tests/                     # Batería de pruebas unitarias y de integración del sistema
```

---

## 🚀 Instalación y Ejecución

### 1. Requisitos Previos
Asegúrate de tener instalado **Python 3.10 o superior** y el gestor de paquetes `pip`.

### 2. Clonar / Descargar el Repositorio
Si aún no lo has hecho, descarga las carpetas del proyecto en tu máquina local.

### 3. Instalar Dependencias
Este juego utiliza la biblioteca **Pillow** para procesar los sprites gráficos con canal alfa (transparencia real). Instálala ejecutando:

```bash
pip install Pillow
```

### 4. Lanzar el Juego
Para iniciar la experiencia gráfica interactiva, simplemente ejecuta el archivo de interfaz principal desde tu terminal en la carpeta raíz del proyecto:

```bash
python Laberinto26/MainInterfaz.py
```

---

## 🎮 Controles del Juego

*   **`W` / `A` / `S` / `D`**: Mover al protagonista por la habitación.
*   **`ESPACIO`**: Blandir la espada (atacar en la dirección a la que miras).
*   **`E`**: Interactuar con los armarios oscuros para abrirlos y conseguir botín (¡cuidado con las trampas!).
*   **`I`**: Abrir/Cerrar el panel de Inventario detallado.
*   **`H` / `U`**: Consumir una poción curativa del inventario para recuperar vida instantáneamente.
*   **`Escape`**: Salir del juego.

---

## 🧪 Ejecución de Pruebas Unitarias

Para garantizar la robustez del código y que todos los patrones funcionan sin errores de integración, se ha provisto una suite de pruebas con `pytest`. 

Para ejecutar los tests automatizados:

1. Instala pytest:
   ```bash
   pip install pytest
   ```
2. Ejecuta los tests en la raíz del proyecto:
   ```bash
   pytest
   ```

---

## 👥 Autores y Licencia
Desarrollado como entrega académica oficial para la asignatura de **Diseño de Software (ESIIAB)**.
*   **Autor**: B1lly05 (GitHub)
*   **Licencia**: Libre uso con fines formativos y de investigación.
