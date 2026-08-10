# Piedra, papel o tijeras

Aplicación de consola desarrollada en Python para jugar a piedra, papel o tijeras contra el programa.

> **Estado:** proyecto en desarrollo. La estructura inicial está creada, pero la interfaz de consola y la lógica de la partida todavía no están implementadas.

## Objetivo

Construir una aplicación CLI sencilla y mantenible que permita al usuario elegir una jugada, generar la respuesta del programa y determinar el resultado de la ronda.

## Características previstas

- Ejecución desde la línea de comandos.
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

## Ejecución

La interfaz CLI aún no está implementada. Cuando esté disponible, el punto de
entrada previsto será:

```powershell
python -m piedra_papel_tijeras.main
```

## Comprobaciones de desarrollo

Con el entorno virtual activo y el proyecto instalado:

```powershell
pytest
ruff check .
mypy src
```

La configuración de estas herramientas se centraliza en `pyproject.toml`. No es
necesario establecer `PYTHONPATH` manualmente.

## Arquitectura del proyecto

La siguiente jerarquía representa la arquitectura objetivo definida para la
aplicación. Incluye tanto los componentes implementados como los previstos.

```text
piedra-papel-tijeras/
|-- src/
|   `-- piedra_papel_tijeras/
|       |-- __init__.py
|       |-- main.py
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
|       `-- test_tipo_jugada.py
|-- docs/
|   |-- guia_pyproject_toml.md
|   |-- diagrama_clases_piedra_papel_tijeras.svg
|   `-- diagrama_flujo_piedra_papel_tijeras.svg
|-- AGENTS.md
|-- pyproject.toml
|-- README.md
`-- requirements.txt
```

Los archivos y subdirectorios utilizan `snake_case`, salvo el directorio raíz del proyecto.

### Estado de la arquitectura

Actualmente están implementados `TipoJugada`, la jerarquía de jugadas, su
fábrica, `Jugador`, `JugadorHumano` y `JugadorMaquina`. `Resultado`, la
coordinación de `Partida` y la interfaz de consola forman parte del diseño
previsto y se implementarán en fases posteriores.

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

- `JugadorHumano`: recibe una elección validada desde la interfaz de consola.
- `JugadorMaquina`: selecciona un `TipoJugada` mediante un generador aleatorio.

Ambos jugadores utilizarán `crear_jugada(tipo)` para obtener una instancia de
`Jugada`, sin construir directamente `Piedra`, `Papel` o `Tijeras`.

El servicio `Partida` coordinará las jugadas, realizará la comparación y devolverá
un valor de `Resultado`: `VICTORIA`, `DERROTA` o `EMPATE`.

```text
main.py
   -> JugadorHumano / JugadorMaquina
   -> crear_jugada(TipoJugada)
   -> Jugada
   -> Partida
   -> Resultado
```

## Documentación

- [Pruebas y calidad](tests/README.md)
- [Guía de configuración de pyproject.toml](docs/guia_pyproject_toml.md)
- [Diagrama de clases](docs/diagrama_clases_piedra_papel_tijeras.svg)
- [Diagrama de flujo](docs/diagrama_flujo_piedra_papel_tijeras.svg)

## Tecnologías

- Python: lenguaje de programación.
- pytest: pruebas automatizadas.
- Ruff: análisis estático y formato.
- mypy: comprobación estática de tipos.
- setuptools: construcción e instalación editable del paquete.
- Git y GitHub: control de versiones y alojamiento remoto.
