# Piedra, papel o tijeras

Aplicación desarrollada en Python para jugar a piedra, papel o tijeras contra
la máquina. El proyecto evolucionó desde una versión funcional de consola hasta
una interfaz gráfica de escritorio construida con PySide6.

El desarrollo aplica una arquitectura modular basada en dominio, herencia,
polimorfismo, creación de objetos mediante una fábrica, servicios, tipado
estático y pruebas automatizadas. La lógica del juego permanece separada de la
interfaz que la utiliza.

## Objetivo

Construir una aplicación mantenible cuyo dominio pueda reutilizarse desde
distintas interfaces:

```text
Dominio del juego
├── Interfaz CLI histórica
└── Interfaz gráfica PySide6 actual
```

La migración a una GUI no sustituye las reglas ya implementadas. PySide6 actúa
como una nueva capa de presentación sobre los mismos modelos y servicios.

## Evolución del proyecto

El proyecto se desarrolló de forma incremental. Cada etapa amplió y consolidó
la anterior:

1. Creación del paquete y del punto de entrada.
2. Modelado de las jugadas mediante abstracción, herencia y polimorfismo.
3. Incorporación de `TipoJugada` y de la fábrica de jugadas.
4. Adopción de `src-layout`, `pyproject.toml` e instalación editable.
5. Construcción progresiva de la batería de pruebas.
6. Incorporación de los jugadores humano y máquina.
7. Implementación de `Partida` y de la versión CLI funcional.
8. Creación del contrato completo `ResultadoDeLaRonda`.
9. Migración de la interacción desde entradas de consola hacia eventos.
10. Construcción de la interfaz PySide6.
11. Incorporación de recursos gráficos y estados visuales.
12. Generación y prueba de un ejecutable mediante PyInstaller.
13. Separación de la documentación visual entre dominio y aplicación.

## Evolución versionada

### `v0.0.0` — Esqueleto inicial

- Estructura inicial del repositorio.
- Creación del paquete `piedra_papel_tijeras`.
- Primer `main.py`.
- README y gestión inicial de dependencias.

### `v0.0.1` — Dominio de las jugadas

- Clase abstracta `Jugada`.
- Implementaciones `Piedra`, `Papel` y `Tijeras`.
- Herencia y polimorfismo.
- Enumeración `TipoJugada`.
- Contrato común `vence_a()`.
- Fábrica `crear_jugada()`.
- Primeras pruebas del dominio.
- Primeros diagramas de clases y flujo.
- Incorporación de `AGENTS.md` como contrato de trabajo.

### `v0.1.0` — Proyecto instalable y pruebas organizadas

- Incorporación de `pyproject.toml`.
- Adopción formal de la estructura `src-layout`.
- Instalación editable del paquete.
- Resolución estable de imports desde `src`.
- Organización jerárquica del directorio `tests`.
- Configuración centralizada de pytest, Ruff y mypy.
- Creación de la guía técnica de `pyproject.toml`.

### `v0.1.1` — Contratos de jugadas verificados

- Baterías completas para Piedra, Papel y Tijeras.
- Pruebas de `TipoJugada`.
- Verificación separada de los valores del enumerado y su representación
  textual.
- Refinamiento del contrato común de `Jugada`.
- Comprobación de las reglas de victoria, derrota y empate.

### `v0.1.2` — Abstracción de jugadores

- Clase abstracta `Jugador`.
- Implementación de `JugadorHumano`.
- Base inicial de `JugadorMaquina`.
- Creación de jugadas delegada a la fábrica.
- Encapsulamiento de la selección humana.
- Pruebas completas de `JugadorHumano`.
- Verificación estática mediante Ruff y mypy.

### `v1.0.0` — Aplicación CLI funcional

- Implementación completa de `JugadorMaquina`.
- Selección aleatoria mediante un generador inyectable.
- Enumeración `Resultado`.
- Servicio `Partida`.
- Resolución de victoria, derrota y empate.
- Bucle principal mediante consola.
- Entrada y validación de la elección humana.
- Pruebas de jugadores, partida, resultado y punto de entrada.

Esta etiqueta representa la primera versión funcional completa del programa.

### `2.0.0` — Aplicación gráfica PySide6

La versión está declarada en `pyproject.toml`, pero todavía no existe la
etiqueta Git `v2.0.0`.

- Incorporación de PySide6.
- Creación de `VentanaDeJuego`.
- Sustitución de entradas de consola por eventos gráficos.
- Componentes y layouts anidados.
- Selección exclusiva mediante `QButtonGroup`.
- Botones representados mediante recursos PNG.
- Activación condicionada del botón «¡Bo!».
- Imágenes diferenciadas para botones, jugadas y resultados.
- Inyección de `JugadorHumano` y `Partida` en la ventana.
- Creación de `ResultadoDeLaRonda`.
- Selección humana de un solo uso mediante `registrar_seleccion()`.
- Presentación retardada del resultado mediante `QTimer`.
- Preparación automática de la siguiente ronda.
- Conservación de `main_consola()` como interfaz histórica.
- Uso de `main()` como entrada gráfica.
- Diagramas separados de dominio y aplicación.
- Preparación del empaquetado mediante PyInstaller.

## Criterio de versionado

El proyecto utiliza versionado semántico:

```text
MAYOR.MENOR.PARCHE
```

- `MAYOR`: cambio funcional o contractual principal.
- `MENOR`: ampliación compatible durante el desarrollo.
- `PARCHE`: refinamiento, corrección o consolidación.

Antes de `1.0.0`, la API se consideraba inestable. Por ello, algunas versiones
`0.x` incorporaron cambios arquitectónicos aun utilizando incrementos de
parche.

El salto principal se resume así:

```text
v1.0.0 → interacción por consola
v2.0.0  → interacción gráfica dirigida por eventos
```

## Características actuales

- Dominio independiente de la interfaz.
- Modelos concretos para Piedra, Papel y Tijeras.
- Fábrica centralizada de jugadas.
- Jugadores humano y máquina bajo una abstracción común.
- Resultado calculado desde la perspectiva humana.
- Interfaz gráfica basada en señales y eventos.
- Recursos gráficos incluidos dentro del paquete.
- Interfaz histórica de consola conservada.
- Pruebas automatizadas con pytest.
- Calidad estática con Ruff y mypy.

## Arquitectura funcional

El punto de entrada gráfico compone los objetos necesarios:

```text
main()
→ QApplication
→ JugadorHumano + JugadorMaquina
→ Partida
→ VentanaDeJuego
→ ciclo de eventos
```

Una ronda completa sigue este flujo:

```text
Seleccionar jugada
→ JugadorHumano.registrar_seleccion(TipoJugada)
→ activar «¡Bo!»
→ Partida.jugar()
→ cada jugador solicita su jugada
→ crear_jugada(TipoJugada)
→ ResultadoDeLaRonda
→ mostrar ambas jugadas
→ QTimer
→ mostrar victoria, derrota o empate
→ preparar la siguiente ronda
```

### Fábrica y jugadores

`Jugador.elegir_jugada()` obtiene un `TipoJugada` mediante el comportamiento
específico del jugador y delega la construcción del objeto a la fábrica:

```text
TipoJugada.PIEDRA  → Piedra()
TipoJugada.PAPEL   → Papel()
TipoJugada.TIJERAS → Tijeras()
```

`JugadorHumano` consume una selección previamente registrada por la interfaz.
`JugadorMaquina` selecciona un tipo mediante un generador aleatorio inyectable.

### Partida y resultado de la ronda

`Partida` coordina ambos jugadores, compara sus jugadas y devuelve un
`ResultadoDeLaRonda` inmutable con:

```text
ResultadoDeLaRonda
├── jugada_humana
├── jugada_maquina
└── resultado
```

El resultado se expresa siempre desde la perspectiva humana: `VICTORIA`,
`DERROTA` o `EMPATE`.

## Interfaz PySide6

`VentanaDeJuego` hereda de `QMainWindow` y organiza la presentación mediante
layouts verticales y horizontales. La ventana:

- Muestra los nombres del jugador y la máquina.
- Agrupa Piedra, Papel y Tijeras como una selección exclusiva.
- Mantiene «¡Bo!» desactivado hasta registrar una jugada válida.
- Muestra las jugadas humana y automática después de ejecutar la ronda.
- Retrasa el resultado central mediante `QTimer.singleShot()`.
- Restablece controles y selección para permitir la siguiente ronda.

### Recursos gráficos

Los recursos se dividen por responsabilidad:

```text
btn_*.png       → iconos de los botones
jugada_*.png    → jugadas reveladas durante la ronda
resultado_*.png → victoria, derrota o empate
```

## Arquitectura del proyecto

```text
python--piedra-papel-tijeras/
├── src/
│   └── piedra_papel_tijeras/
│       ├── __init__.py
│       ├── main.py
│       ├── gui/
│       │   ├── __init__.py
│       │   └── ventana_de_juego.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── tipo_jugada.py
│       │   ├── resultado.py
│       │   ├── resultado_ronda.py
│       │   ├── jugadas/
│       │   │   ├── fabrica_jugadas.py
│       │   │   ├── jugada.py
│       │   │   ├── papel.py
│       │   │   ├── piedra.py
│       │   │   └── tijeras.py
│       │   └── jugadores/
│       │       ├── jugador.py
│       │       ├── jugador_humano.py
│       │       └── jugador_maquina.py
│       ├── services/
│       │   └── partida.py
│       └── resources/
│           ├── btn_*.png
│           ├── jugada_*.png
│           └── resultado_*.png
├── tests/
│   ├── README.md
│   ├── test_main.py
│   ├── models/
│   └── services/
├── docs/
│   ├── guia_pyproject_toml.md
│   ├── diagrama_interfaz.png
│   ├── diagrama_clases_piedra_papel_tijeras.svg
│   ├── diagrama_clases_aplicacion_pyside6.svg
│   ├── diagrama_flujo_piedra_papel_tijeras.svg
│   └── diagrama_flujo_aplicacion_pyside6.svg
├── AGENTS.md
├── pyproject.toml
└── README.md
```

## Requisitos

- Python 3.14 o superior.
- pip.

## Instalación

Crear y activar un entorno virtual en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar el proyecto en modo editable junto con las herramientas de desarrollo:

```powershell
python -m pip install -e ".[dev]"
```

La instalación editable registra el paquete dentro del entorno, pero mantiene
el código fuente en `src`. Los cambios en los módulos quedan disponibles sin
reinstalar el proyecto.

## Ejecución

### Interfaz gráfica actual

Después de instalar el proyecto:

```powershell
piedra-papel-tijeras
```

También puede iniciarse mediante:

```powershell
python -m piedra_papel_tijeras.main
```

### Interfaz histórica de consola

La lógica de consola permanece disponible en `main_consola()`, pero no
constituye el punto de entrada predeterminado.

## Pruebas y calidad

Con el entorno virtual activo y el grupo `dev` instalado:

```powershell
pytest
ruff check .
mypy src
```

Las pruebas reproducen la organización del código productivo y cubren jugadas,
fábrica, tipos, jugadores, partida, resultados y entrada de consola.

Durante el escalado hacia la GUI quedó registrada una verificación con 58
pruebas superadas, Ruff sin incidencias y 20 módulos comprobados con mypy. Esta
cifra representa ese hito histórico y debe volver a verificarse antes de cada
publicación.

## Generación del ejecutable

Durante el escalado se generó correctamente un ejecutable para Windows mediante
PyInstaller. El proceso requirió definir correctamente el nombre de salida y
gestionar la interferencia del antivirus durante la construcción.

PyInstaller permanece como dependencia de desarrollo porque no es necesario
para ejecutar el proyecto desde el código fuente.

La configuración concreta de construcción deberá coincidir con los archivos
presentes en el repositorio antes de publicar una nueva versión.

## Documentación visual

El proyecto conserva dos niveles complementarios:

### Dominio

- [Diagrama de clases del dominio](docs/diagrama_clases_piedra_papel_tijeras.svg)
- [Diagrama de flujo del dominio](docs/diagrama_flujo_piedra_papel_tijeras.svg)

Estos diagramas explican las reglas y relaciones independientes de la interfaz.

### Aplicación PySide6

- [Diagrama de clases de la aplicación](docs/diagrama_clases_aplicacion_pyside6.svg)
- [Diagrama de flujo de la aplicación](docs/diagrama_flujo_aplicacion_pyside6.svg)
- [Diseño de referencia de la interfaz](docs/diagrama_interfaz.png)

Estos recursos incorporan `main()`, `VentanaDeJuego`, controles Qt, eventos,
inyección de dependencias, temporización y representación gráfica del resultado.

## Documentación técnica

- [Guía de configuración de pyproject.toml](docs/guia_pyproject_toml.md)
- [Guía de pruebas](tests/README.md)

## Tecnologías

- Python: lenguaje principal.
- PySide6: interfaz gráfica de escritorio.
- pytest: pruebas automatizadas.
- Ruff: análisis estático y convenciones.
- mypy: comprobación estática de tipos.
- setuptools: construcción e instalación del paquete.
- PyInstaller: generación del ejecutable de Windows.
- Git y GitHub: versionado y publicación del código.
