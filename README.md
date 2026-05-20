# 🏛️ Laberinto26 Python

¡Bienvenido al repositorio de **Laberinto26**! 

Este proyecto es un juego de exploración de laberintos desarrollado en Python. El jugador asume el papel de un protagonista que debe navegar por distintas habitaciones, interactuar con objetos (armarios, puertas, cofres), enfrentarse a enemigos ("Bichos", "Guardianes") y sobrevivir utilizando ítems como pociones y armaduras, todo en su camino para encontrar tesoros legendarios como la *Espada del Olimpo*.

Más allá de ser un juego, este proyecto destaca por ser una **excelente implementación de Arquitectura de Software**, aplicando múltiples patrones de diseño clásicos (GoF) para mantener un código limpio, escalable y modular.

---

## 🚀 Características Principales

* **Exploración de Mazmorras:** Navega a través de habitaciones conectadas por puertas y túneles en múltiples direcciones (Norte, Sur, Este, Oeste y diagonales).
* **Sistema de Combate e Interacción:** Ataca enemigos, abre puertas (si tienes la llave adecuada) y saquea contenedores.
* **Sistema de Estados:** Las puertas pueden estar abiertas o cerradas; las entidades pueden estar vivas o muertas.
* **Inteligencia Artificial de Enemigos:** Los monstruos tienen modos de comportamiento (Agresivo, Perezoso) que dictan cómo actúan frente al jugador.
* **Trampas y Entornos Dinámicos:** Paredes bomba, armarios con veneno y elementos destructibles.
* **Interfaz:** Soporte para ejecución e interfaz gráfica (usando los recursos de la carpeta `assets`).
* **Carga de Mapas:** Generación de laberintos predefinidos a través de archivos `.json` (ej. *Laberinto Del Olimpo.json*).

---

## 🧩 Patrones de Diseño Implementados

El código base está fuertemente orientado a objetos y utiliza los siguientes patrones de diseño:

### 1. Patrones Creacionales
* **Builder (`Laberinto26_builder/`)**: Se utiliza para separar la construcción del laberinto (habitaciones, paredes, puertas) de su representación. Facilita la creación de diferentes tipos de laberintos (ej. `LaberintoBuilderRombo`).

### 2. Patrones Estructurales
* **Composite (`ElementosFisicos/`)**: Permite tratar a los elementos individuales (Pared, Puerta, Cuadrado, Rombo) y a las composiciones de elementos (Habitacion, Laberinto, Contenedor) de manera uniforme a través de la clase base `ElementoMapa`.
* **Decorator (`ElementosFisicos/Decorator.py`)**: Añade responsabilidades o características adicionales a los elementos físicos dinámicamente (por ejemplo, para bombas o estados alterados).

### 3. Patrones de Comportamiento
* **Command (`Comandos/`)**: Encapsula todas las acciones del jugador (`Abrir`, `Atacar`, `Interactuar`, `UsarPocion`) como objetos, permitiendo un fácil manejo, encolamiento o deshacer acciones.
* **State (`Estados/`)**: Controla el comportamiento de los objetos dependiendo de su estado interno. Usado en entidades (`Vivo`, `Muerto`) y elementos del entorno (`Abierta`, `Cerrada` para las puertas).
* **Strategy (`Entidades/Modo.py`, `Agresivo.py`, `Perezoso.py`)**: Define el comportamiento intercambiable de los enemigos en el laberinto.
* **Visitor (`Visitor/`)**: Permite separar los algoritmos de la estructura de objetos sobre la que operan. Útil para aplicar efectos globales sobre el laberinto sin modificar las clases de los elementos (ej. `VisitorAbrirPuertas`, `VisitorActivarBombas`).


# Diagrama de secuencia

<img width="8192" height="5676" alt="Visitor Composite Flow-2026-05-20-173614" src="https://github.com/user-attachments/assets/ae77a932-77e7-47bd-8968-90dfcdfd7840" />


---

## 📁 Estructura del Proyecto

```text
📦 Laberinto26Phyton
 ┣ 📂 Laberinto26/
 ┃ ┣ 📂 Comandos/         # Lógica de acciones del jugador (Atacar, Abrir, etc.)
 ┃ ┣ 📂 ElementosFisicos/ # Componentes del mapa (Pared, Puerta, Habitacion, etc.)
 ┃ ┣ 📂 Entidades/        # Clases de personajes (Prota, Bicho, Guardian) y comportamientos
 ┃ ┣ 📂 Estados/          # Lógica de estados para entidades y puertas
 ┃ ┣ 📂 Orientaciones/    # Vectores y direcciones de movimiento
 ┃ ┣ 📂 Visitor/          # Operaciones masivas sobre el laberinto
 ┃ ┣ 📂 assets/           # Sprites e imágenes para la interfaz gráfica
 ┃ ┣ 📜 Juego.py          # Lógica central (Game Engine)
 ┃ ┣ 📜 Main.py           # Punto de entrada por consola
 ┃ ┗ 📜 MainInterfaz.py   # Punto de entrada con Interfaz Gráfica
 ┣ 📂 Laberinto26_builder/# Constructores de mapas y Director
 ┣ 📂 Mapa/               # Mapas en formato JSON
 ┗ 📂 tests/              # Pruebas unitarias para garantizar el funcionamiento





