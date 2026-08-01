# Piedra, papel o tijeras

Aplicación de consola desarrollada en Python para jugar a piedra, papel o tijeras contra el programa.

> **Estado:** proyecto en desarrollo. La estructura inicial está creada, pero la interfaz de consola y la lógica de la partida todavía no están implementadas.

## Objetivo

Construir una aplicación CLI sencilla y mantenible que permita al usuario elegir una jugada, generar la respuesta del programa y determinar el resultado de la ronda.

## Características previstas

- Ejecución desde la línea de comandos.
- Modelos independientes para piedra, papel y tijeras.
- Lógica de partida separada de la interacción con el usuario.
- Pruebas automatizadas con pytest.
- Análisis estático y formato mediante Ruff.
- Comprobación de tipos con mypy.

## Requisitos

- Python 3.
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

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

La interfaz CLI aún no está implementada. Cuando esté disponible, el punto de entrada previsto será:

```bash
python -m piedra_papel_tijeras.main
```

## Estructura del proyecto

```text
piedra-papel-tijeras/
|-- src/
|   `-- piedra_papel_tijeras/
|       |-- __init__.py
|       |-- main.py
|       |-- models/
|       |   |-- __init__.py
|       |   |-- jugada.py
|       |   |-- papel.py
|       |   |-- piedra.py
|       |   `-- tijeras.py
|       `-- services/
|           |-- __init__.py
|           `-- partida.py
|-- tests/
|   |-- README.md
|   |-- test_jugada.py
|   |-- test_papel.py
|   |-- test_piedra.py
|   `-- test_tijeras.py
|-- docs/
|   |-- diagrama_clases_piedra_papel_tijeras.svg
|   `-- diagrama_flujo_piedra_papel_tijeras.svg
|-- AGENTS.md
|-- README.md
`-- requirements.txt
```

Los archivos y subdirectorios utilizan `snake_case`, salvo el directorio raíz del proyecto.

## Documentación

- [Pruebas y calidad](tests/README.md)
- [Diagrama de clases](docs/diagrama_clases_piedra_papel_tijeras.svg)
- [Diagrama de flujo](docs/diagrama_flujo_piedra_papel_tijeras.svg)

## Tecnologías

- Python: lenguaje de programación.
- pytest: pruebas automatizadas.
- Ruff: análisis estático y formato.
- mypy: comprobación estática de tipos.
- Git y GitHub: control de versiones y alojamiento remoto.
