# Guía de configuración de `pyproject.toml`

## 1. Finalidad

`pyproject.toml` es el archivo estándar de configuración de un proyecto Python.

Permite centralizar:

- Los metadatos del proyecto.
- La versión mínima de Python.
- Las dependencias de ejecución y desarrollo.
- El sistema de construcción.
- La ubicación de los paquetes.
- La configuración de pytest, Ruff y mypy.
- Los futuros comandos de consola.

En este proyecto también permite que Python encuentre correctamente el paquete:

```text
src/
└── piedra_papel_tijeras/
```

De esta forma, los módulos pueden importarse mediante:

```python
from piedra_papel_tijeras.models import ...
```

## 2. Ubicación

El archivo debe estar en la raíz del repositorio:

```text
python--piedra-papel-tijeras/
├── pyproject.toml
├── README.md
├── requirements.txt
├── src/
└── tests/
```

## 3. Plantilla adaptada al proyecto

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "piedra-papel-tijeras"
version = "0.0.1"
description = "Aplicación de consola para jugar a piedra, papel o tijeras"
readme = "README.md"
requires-python = ">=3.14"

keywords = [
    "python",
    "cli",
    "juego",
    "piedra-papel-tijeras",
]

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.14",
    "Operating System :: OS Independent",
    "Typing :: Typed",
]

dependencies = []

[project.optional-dependencies]
dev = [
    "pytest==9.1.1",
    "ruff==0.16.1",
    "mypy==2.3.0",
]

[tool.setuptools.packages.find]
where = ["src"]
include = ["piedra_papel_tijeras*"]
namespaces = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
pythonpath = ["src"]
addopts = "-ra"

[tool.ruff]
target-version = "py314"
line-length = 88
src = ["src", "tests"]

[tool.mypy]
python_version = "3.14"
strict = true
mypy_path = "src"
```

## 4. Sistema de construcción

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
```

Esta sección indica que el proyecto será construido e instalado mediante
`setuptools`.

- `requires`: herramientas necesarias para construir el paquete.
- `build-backend`: componente encargado de realizar la construcción.

## 5. Metadatos del proyecto

```toml
[project]
name = "piedra-papel-tijeras"
version = "0.0.1"
description = "Aplicación de consola para jugar a piedra, papel o tijeras"
readme = "README.md"
requires-python = ">=3.14"
```

- `name`: nombre utilizado por las herramientas de instalación.
- `version`: versión actual del proyecto.
- `description`: descripción breve.
- `readme`: documento principal del proyecto.
- `requires-python`: versiones de Python admitidas.

El nombre de distribución puede contener guiones:

```text
piedra-papel-tijeras
```

El paquete utilizado en los imports conserva guiones bajos:

```python
import piedra_papel_tijeras
```

## 6. Dependencias de ejecución

```toml
dependencies = []
```

Aquí se declaran únicamente las bibliotecas necesarias para ejecutar la
aplicación. Actualmente, el proyecto utiliza la biblioteca estándar de Python.

Ejemplo futuro:

```toml
dependencies = [
    "nombre-paquete>=1.0",
]
```

## 7. Dependencias de desarrollo

```toml
[project.optional-dependencies]
dev = [
    "pytest==9.1.1",
    "ruff==0.16.1",
    "mypy==2.3.0",
]
```

El grupo `dev` contiene herramientas necesarias durante el desarrollo, pero no
para ejecutar la aplicación.

Su instalación se solicita mediante:

```powershell
python -m pip install -e ".[dev]"
```

Interpretación:

```text
.       → proyecto situado en el directorio actual
[dev]   → grupo opcional de dependencias de desarrollo
-e      → instalación editable
```

## 8. Descubrimiento del paquete

```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["piedra_papel_tijeras*"]
namespaces = false
```

Esta sección indica que los paquetes se encuentran dentro de `src`. El patrón
incluye el paquete principal y sus subpaquetes:

```text
piedra_papel_tijeras
piedra_papel_tijeras.models
piedra_papel_tijeras.models.jugadas
piedra_papel_tijeras.services
```

## 9. Configuración de pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
pythonpath = ["src"]
addopts = "-ra"
```

- `testpaths`: directorios donde pytest buscará pruebas.
- `python_files`: patrón utilizado para identificar módulos de pruebas.
- `pythonpath`: incorpora `src` a la ruta de importación durante las pruebas.
- `addopts`: opciones aplicadas automáticamente en cada ejecución.

Ejecutar todas las pruebas:

```powershell
pytest
```

Ejecutar una prueba concreta:

```powershell
pytest tests/models/jugadas/test_jugada.py
```

## 10. Configuración de Ruff

```toml
[tool.ruff]
target-version = "py314"
line-length = 88
src = ["src", "tests"]
```

Ruff comprueba el estilo y determinados errores estáticos:

```powershell
ruff check .
```

## 11. Configuración de mypy

```toml
[tool.mypy]
python_version = "3.14"
strict = true
mypy_path = "src"
```

mypy comprueba las anotaciones de tipos:

```powershell
mypy src
```

El modo estricto puede revelar errores adicionales a medida que crezca el
proyecto.

## 12. Preparación del entorno virtual

Crear el entorno:

```powershell
python -m venv .venv
```

Activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar el proyecto y las herramientas de desarrollo:

```powershell
python -m pip install -e ".[dev]"
```

No deben editarse manualmente los archivos internos de `.venv`.

## 13. Instalación editable

La opción `-e` registra el proyecto dentro de `.venv`, manteniendo el código
fuente en `src`. Los cambios realizados en los módulos estarán disponibles sin
reinstalar el proyecto.

Debe repetirse la instalación cuando cambien:

- Las dependencias.
- Los grupos opcionales.
- Los comandos de consola.
- El sistema de construcción.
- Determinados metadatos del proyecto.

```powershell
python -m pip install -e ".[dev]"
```

## 14. Verificación

Comprobar el intérprete:

```powershell
python -c "import sys; print(sys.executable)"
```

Debe apuntar a:

```text
.venv\Scripts\python.exe
```

Comprobar el paquete:

```powershell
python -c "import piedra_papel_tijeras; print(piedra_papel_tijeras.__file__)"
```

Debe apuntar a:

```text
src\piedra_papel_tijeras\__init__.py
```

Ejecutar las comprobaciones:

```powershell
pytest
ruff check .
mypy src
```

## 15. Actualización de versiones

No es necesario modificar la versión por cada cambio o commit.

Ejemplo de evolución:

```text
0.0.1 → estructura y modelos iniciales
0.1.0 → primera versión funcional
0.2.0 → incorporación de nuevas funcionalidades
0.2.1 → corrección compatible
1.0.0 → primera versión estable
```

La versión debe actualizarse cuando se prepare una nueva entrega identificable.

## 16. Futuro comando de consola

Cuando `main.py` defina una función ejecutable:

```python
def main() -> None:
    ...
```

podrá añadirse:

```toml
[project.scripts]
piedra-papel-tijeras = "piedra_papel_tijeras.main:main"
```

Después de reinstalar:

```powershell
python -m pip install -e ".[dev]"
```

la aplicación podrá iniciarse con:

```powershell
piedra-papel-tijeras
```

## 17. Resolución de problemas

### No se encuentra `piedra_papel_tijeras`

```text
ModuleNotFoundError: No module named 'piedra_papel_tijeras'
```

Reinstalar el proyecto:

```powershell
python -m pip install -e ".[dev]"
```

### No se reconoce pytest

Activar `.venv`:

```powershell
.\.venv\Scripts\Activate.ps1
```

Ejecutar pytest mediante Python:

```powershell
python -m pytest
```

### VS Code subraya los imports

Seleccionar el intérprete:

```text
Python: Select Interpreter
→ .venv\Scripts\python.exe
```

Después, reiniciar el servidor de lenguaje de Python.

## 18. Mantenimiento de `pyproject.toml`

El archivo no se modifica con cada cambio de código. Debe actualizarse cuando
cambien:

| Cambio | Sección afectada |
| --- | --- |
| Nueva publicación | `project.version` |
| Nueva dependencia de ejecución | `project.dependencies` |
| Nueva herramienta de desarrollo | `project.optional-dependencies` |
| Versiones de Python admitidas | `requires-python` |
| Nuevo comando de consola | `project.scripts` |
| Estructura de paquetes | `tool.setuptools` |
| Comportamiento de las pruebas | `tool.pytest` |
| Reglas de análisis | `tool.ruff` o `tool.mypy` |

## 19. Referencias

- [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Configuración de setuptools](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
- [Estructura `src-layout`](https://setuptools.pypa.io/en/stable/userguide/package_discovery.html)
- [Configuración de pytest](https://docs.pytest.org/en/stable/reference/customize.html)
