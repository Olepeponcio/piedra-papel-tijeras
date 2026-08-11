# Piedra, papel o tijeras

Aplicación desarrollada en Python para jugar a piedra, papel o tijeras contra el
programa. La versión de consola permanece disponible mientras el proyecto escala
hacia una interfaz gráfica de escritorio con PySide6.

> **Estado:** versión `v1.0.0` de consola funcional y evolución gráfica con
> PySide6 en desarrollo.

## Objetivo

Construir una aplicación mantenible que permita ejecutar el mismo dominio desde
distintas interfaces. La consola constituye la primera interfaz funcional y
PySide6 será la siguiente capa de presentación.

## Características previstas

- Ejecución desde la línea de comandos.
- Interfaz gráfica de escritorio con PySide6 en desarrollo.
- Modelos independientes para piedra, papel y tijeras.
- Creación centralizada de jugadas a partir de `TipoJugada`.
- Lógica de partida separada de la interacción con el usuario.
- Pruebas automatizadas con pytest.
- Análisis estático y formato mediante Ruff.
- Comprobación de tipos con mypy.

## Requisitos

- Python 3.14 o superior.
- pip.

## Instalación

Se recomienda utilizar un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala el proyecto en modo editable junto con las herramientas de desarrollo:

```powershell
python -m pip install -e ".[dev]"
```

La instalación editable conecta el entorno virtual con el código de `src`, por
lo que los cambios en los módulos quedan disponibles sin reinstalar el paquete.

## Ejecución de la versión de consola

Ejecuta una ronda desde la interfaz de consola:

```powershell
python -m piedra_papel_tijeras.main
```

La ejecución histórica permanece disponible mediante `main_consola()`. La entrada
`main()` inicia actualmente la interfaz PySide6.

## Evolución hacia PySide6

La nueva interfaz sustituye la lectura de la jugada mediante `input()` por eventos
de botones. `JugadorHumano` registra temporalmente un `TipoJugada` y lo consume al
crear la siguiente jugada:

```text
Consola o GUI
    -> JugadorHumano.registrar_seleccion(TipoJugada)
    -> JugadorHumano.elegir_jugada()
    -> JugadorHumano._seleccionar_tipo()
    -> crear_jugada(TipoJugada)
    -> Partida.jugar()
```

Este cambio elimina el selector basado en `lambda` del modelo. La consola solicita
el tipo antes de registrarlo y la ventana lo registra cuando el usuario pulsa
Piedra, Papel o Tijeras. La selección es de un solo uso: después de construir la
jugada concreta, debe registrarse otra para ejecutar una nueva ronda.

La ventana en desarrollo se encuentra en
`src/piedra_papel_tijeras/gui/ventana_de_juego.py` y constituye la entrada
principal actual. La función `main_consola()` conserva el proceso previo.

El proyecto conserva dos niveles de documentación visual:

- [Flujo del dominio](docs/diagrama_flujo_piedra_papel_tijeras.svg): describe
  las reglas del juego desde una elección hasta victoria, derrota o empate, sin
  depender de una interfaz concreta.
- [Flujo de la aplicación PySide6](docs/diagrama_flujo_aplicacion_pyside6.svg):
  amplía el flujo con `main_pyside6()`, `VentanaDeJuego`, señales, fábrica,
  `ResultadoDeLaRonda`, `QTimer` y preparación de la siguiente ronda.

El flujo del dominio se mantiene estable y reutilizable. El flujo de aplicación
se amplía conforme aparecen nuevas formas de interacción o coordinación.

La misma separación se aplica a los diagramas de clases:

- [Clases del dominio](docs/diagrama_clases_piedra_papel_tijeras.svg): documenta
  jugadores, jugadas, fábrica, partida y objetos de resultado sin depender de Qt.
- [Clases de la aplicación PySide6](docs/diagrama_clases_aplicacion_pyside6.svg):
  añade `main_pyside6()`, `VentanaDeJuego`, controles Qt, inyección de dependencias
  y las relaciones con el dominio reutilizable.

## Comprobaciones de desarrollo

Con el entorno virtual activo y el proyecto instalado:

```powershell
pytest
ruff check .
mypy src
```

La configuración de estas herramientas se centraliza en `pyproject.toml`. No es
necesario establecer `PYTHONPATH` manualmente.

## Generación del ejecutable

El ejecutable para Windows se genera con PyInstaller. Con el entorno virtual
activo y las dependencias de desarrollo instaladas, ejecuta desde la raíz del
proyecto:

```powershell
pyinstaller --clean --noconfirm main.spec
```

El archivo resultante se crea en:

```text
dist/main.exe
```

Durante la construcción, PyInstaller utiliza:

- `main.spec`: configuración de entrada y opciones del ejecutable.
- `build/`: archivos temporales de construcción.
- `dist/`: resultado distribuible.

`build/` puede eliminarse después de generar el ejecutable. Para comprobar el
resultado, ejecuta:

```powershell
.\dist\main.exe
```

## Arquitectura del proyecto

La siguiente jerarquía representa la arquitectura objetivo definida para la
aplicación. Incluye tanto los componentes implementados como los previstos.

```text
piedra-papel-tijeras/
|-- src/
|   `-- piedra_papel_tijeras/
|       |-- __init__.py
|       |-- main.py
|       |-- gui/
|       |   |-- __init__.py
|       |   |-- ventana_de_juego.py
|       |   `-- ventana_principal.py
|       |-- resources/
|       |   |-- btn_papel.png
|       |   |-- btn_piedra.png
|       |   `-- btn_tijeras.png
|       |-- models/
|       |   |-- __init__.py
|       |   |-- tipo_jugada.py
|       |   |-- resultado.py
|       |   |-- jugadas/
|       |   |   |-- __init__.py
|       |   |   |-- fabrica_jugadas.py
|       |   |   |-- jugada.py
|       |   |   |-- papel.py
|       |   |   |-- piedra.py
|       |   |   `-- tijeras.py
|       |   `-- jugadores/
|       |       |-- __init__.py
|       |       |-- jugador.py
|       |       |-- jugador_humano.py
|       |       `-- jugador_maquina.py
|       `-- services/
|           |-- __init__.py
|           `-- partida.py
|-- tests/
|   |-- README.md
|   |-- test_main.py
|   |-- services/
|   |   `-- test_partida.py
|   `-- models/
|       |-- jugadas/
|       |   |-- test_fabrica_jugadas.py
|       |   |-- test_jugada.py
|       |   |-- test_papel.py
|       |   |-- test_piedra.py
|       |   `-- test_tijeras.py
|       |-- jugadores/
|       |   |-- test_jugador_humano.py
|       |   `-- test_jugador_maquina.py
|       |-- test_resultado.py
|       `-- test_tipo_jugada.py
|-- docs/
|   |-- guia_pyproject_toml.md
|   |-- diagrama_clases_piedra_papel_tijeras.svg
|   |-- diagrama_clases_aplicacion_pyside6.svg
|   |-- diagrama_flujo_piedra_papel_tijeras.svg
|   `-- diagrama_flujo_aplicacion_pyside6.svg
|-- AGENTS.md
|-- pyproject.toml
|-- README.md
`-- requirements.txt
```

Los archivos y subdirectorios utilizan `snake_case`, salvo el directorio raíz del proyecto.

### Estado de la arquitectura

Actualmente están implementados `TipoJugada`, `Resultado`, la jerarquía de
jugadas, su fábrica, los jugadores, la coordinación de `Partida` y la interfaz
de consola para ejecutar una ronda. La ventana PySide6 está en desarrollo y
reutilizará el mismo dominio.

## Modelos de jugada

El paquete `models/jugadas` contiene la abstracción `Jugada` y sus implementaciones
`Piedra`, `Papel` y `Tijeras`. Cada implementación conserva la responsabilidad de
declarar su tipo y la jugada a la que vence.

La función `crear_jugada(tipo)` de `fabrica_jugadas.py` convierte un `TipoJugada`
en la instancia concreta correspondiente. De esta forma, los futuros jugadores y
servicios podrán solicitar una `Jugada` sin encargarse de elegir su clase concreta.

```text
TipoJugada.PIEDRA  -> Piedra()
TipoJugada.PAPEL   -> Papel()
TipoJugada.TIJERAS -> Tijeras()
```

## Jugadores, partida y resultado

El paquete `models/jugadores` agrupa la abstracción `Jugador` y sus dos
implementaciones:

- `JugadorHumano`: registra una elección validada recibida desde la interfaz
  activa y la consume al crear una única jugada.
- `JugadorMaquina`: selecciona un `TipoJugada` mediante un generador aleatorio.

Ambos jugadores utilizarán `crear_jugada(tipo)` para obtener una instancia de
`Jugada`, sin construir directamente `Piedra`, `Papel` o `Tijeras`.

El servicio `Partida` coordina las jugadas, realiza la comparación y devuelve un
`ResultadoDeLaRonda` con ambas jugadas y un `Resultado` desde la perspectiva
humana: `VICTORIA`, `DERROTA` o `EMPATE`.

```text
main.py
   -> JugadorHumano.registrar_seleccion(TipoJugada)
   -> JugadorHumano / JugadorMaquina
   -> Jugador.elegir_jugada()
   -> crear_jugada(TipoJugada)
   -> Jugada
   -> Partida
   -> ResultadoDeLaRonda
```

## Documentación

- [Pruebas y calidad](tests/README.md)
- [Guía de configuración de pyproject.toml](docs/guia_pyproject_toml.md)
- [Diagrama de clases del dominio](docs/diagrama_clases_piedra_papel_tijeras.svg)
- [Diagrama de clases de la aplicación PySide6](docs/diagrama_clases_aplicacion_pyside6.svg)
- [Diagrama de flujo del dominio](docs/diagrama_flujo_piedra_papel_tijeras.svg)
- [Diagrama de flujo de la aplicación PySide6](docs/diagrama_flujo_aplicacion_pyside6.svg)

## Tecnologías

- Python: lenguaje de programación.
- PySide6: interfaz gráfica de escritorio en desarrollo.
- pytest: pruebas automatizadas.
- Ruff: análisis estático y formato.
- mypy: comprobación estática de tipos.
- setuptools: construcción e instalación editable del paquete.
- Git y GitHub: control de versiones y alojamiento remoto.
