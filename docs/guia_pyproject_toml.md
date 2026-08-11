# Guía de configuración de `pyproject.toml`

## 1. Finalidad

`pyproject.toml` es el archivo estándar que describe cómo se construye, instala,
ejecuta y verifica el proyecto Python.

En este repositorio centraliza:

- El sistema de construcción.
- Los metadatos y la versión del programa.
- La versión mínima de Python.
- Las dependencias de ejecución y desarrollo.
- La ubicación del paquete dentro de `src`.
- El comando de inicio de la aplicación.
- Los recursos gráficos incluidos en el paquete.
- La configuración de pytest, Ruff y mypy.

## 2. Evolución de la configuración

El proyecto comenzó con una estructura mínima y un `requirements.txt`. A medida
que crecieron el dominio y las pruebas, aparecieron problemas para importar el
paquete situado dentro de `src`.

Durante el desarrollo se utilizaron soluciones temporales mediante
`PYTHONPATH`. La solución estable fue convertir el repositorio en un proyecto
instalable mediante `pyproject.toml` y registrarlo en el entorno virtual en modo
editable.

La evolución fue:

```text
requirements.txt inicial
→ problemas de imports desde src
→ PYTHONPATH temporal
→ creación de pyproject.toml
→ instalación editable
→ grupo opcional dev
→ incorporación de PySide6
→ comando ejecutable
→ declaración de recursos PNG
→ retirada de requirements.txt
```

## 3. Ubicación

El archivo se encuentra en la raíz:

```text
python--piedra-papel-tijeras/
├── pyproject.toml
├── README.md
├── src/
├── tests/
└── docs/
```

## 4. Configuración adaptada a la versión gráfica

La configuración debe representar el estado de la aplicación PySide6:

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "piedra-papel-tijeras"
version = "2.0.0"
description = "Aplicación gráfica de escritorio para jugar a piedra, papel o tijeras"
readme = "README.md"
requires-python = ">=3.14"

keywords = [
    "python",
    "gui",
    "juego",
    "pyside6",
    "piedra-papel-tijeras",
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Win32 (MS Windows)",
    "Intended Audience :: End Users/Desktop",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.14",
    "Operating System :: Microsoft :: Windows",
]

dependencies = [
    "PySide6==6.11.1",
]

[project.optional-dependencies]
dev = [
    "mypy==2.3.0",
    "pyinstaller==6.22.0",
    "pytest==9.1.1",
    "ruff==0.16.1",
]

[project.scripts]
piedra-papel-tijeras = "piedra_papel_tijeras.main:main"

[tool.setuptools.packages.find]
where = ["src"]
include = ["piedra_papel_tijeras*"]
namespaces = false

[tool.setuptools.package-data]
piedra_papel_tijeras = ["resources/*.png"]

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

Este bloque documenta la configuración objetivo de la versión gráfica. Los
cambios sobre el archivo real deben revisarse y autorizarse de forma separada.

## 5. Sistema de construcción

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"
```

`setuptools` se encarga de descubrir, construir e instalar el paquete.

## 6. Metadatos y nombres

El nombre de distribución puede utilizar guiones:

```text
piedra-papel-tijeras
```

El paquete importable conserva guiones bajos:

```python
import piedra_papel_tijeras
```

Son identificadores relacionados, pero cumplen funciones distintas:

```text
piedra-papel-tijeras → distribución y comando
piedra_papel_tijeras → paquete de Python
```

## 7. Dependencias de ejecución

```toml
dependencies = [
    "PySide6==6.11.1",
]
```

PySide6 es una dependencia de ejecución porque `main.py` y
`ventana_de_juego.py` la importan para iniciar y representar la interfaz.

Una instalación normal debe obtenerla automáticamente:

```powershell
python -m pip install .
```

## 8. Dependencias de desarrollo

```toml
[project.optional-dependencies]
dev = [
    "mypy==2.3.0",
    "pyinstaller==6.22.0",
    "pytest==9.1.1",
    "ruff==0.16.1",
]
```

Estas herramientas no son necesarias para ejecutar la aplicación:

```text
pytest      → pruebas automatizadas
Ruff        → análisis estático y convenciones
mypy        → comprobación de tipos
PyInstaller → construcción del ejecutable
```

Se instalan mediante:

```powershell
python -m pip install -e ".[dev]"
```

Interpretación:

```text
.       → proyecto situado en el directorio actual
[dev]   → grupo opcional de desarrollo
-e      → instalación editable
```

## 9. Instalación editable

La instalación editable registra el proyecto dentro del entorno virtual, pero
mantiene el código fuente en `src`. Los cambios realizados en los módulos se
reflejan sin reinstalar el paquete.

Debe repetirse cuando cambien:

- Las dependencias.
- Los grupos opcionales.
- Los comandos ejecutables.
- El sistema de construcción.
- Los datos incluidos en el paquete.

```powershell
python -m pip install -e ".[dev]"
```

## 10. Por qué aparece el proyecto en `pip list`

Después de instalarlo en modo editable, `pip list` muestra una entrada similar
a esta:

```text
Package                 Version  Editable project location
piedra-papel-tijeras    2.0.0    C:\ruta\del\proyecto
```

No es una dependencia externa ni una copia del repositorio. Es el paquete local
registrado en el entorno y enlazado con su código fuente.

## 11. Retirada de `requirements.txt`

`requirements.txt` se utilizó durante las primeras etapas. Posteriormente quedó
redundante porque las dependencias pasaron a estar centralizadas en
`pyproject.toml`.

Instalación de la aplicación:

```powershell
python -m pip install .
```

Instalación para desarrollar:

```powershell
python -m pip install -e ".[dev]"
```

Las dependencias transitivas de PySide6, pytest, Ruff, mypy y PyInstaller se
resuelven automáticamente y no deben copiarse manualmente a otro archivo.

## 12. Descubrimiento del paquete

```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["piedra_papel_tijeras*"]
namespaces = false
```

La configuración descubre el paquete principal y sus subpaquetes:

```text
piedra_papel_tijeras
├── gui
├── models
│   ├── jugadas
│   └── jugadores
└── services
```

El directorio `src` es un contenedor de código, no el nombre del paquete.

## 13. Recursos gráficos

Los PNG no son módulos Python. Deben declararse como datos del paquete:

```toml
[tool.setuptools.package-data]
piedra_papel_tijeras = ["resources/*.png"]
```

Esto permite incluir:

```text
resources/
├── btn_*.png
├── jugada_*.png
└── resultado_*.png
```

Sin esta declaración, una distribución construida podría instalar el código sin
las imágenes necesarias para la interfaz.

## 14. Comando ejecutable

```toml
[project.scripts]
piedra-papel-tijeras = "piedra_papel_tijeras.main:main"
```

Después de instalar o reinstalar el proyecto:

```powershell
piedra-papel-tijeras
```

invoca la función `main()` del módulo `piedra_papel_tijeras.main`.

También puede utilizarse:

```powershell
python -m piedra_papel_tijeras.main
```

## 15. Configuración de pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
pythonpath = ["src"]
addopts = "-ra"
```

- `testpaths`: limita la búsqueda al directorio de pruebas.
- `python_files`: define el patrón de módulos de prueba.
- `pythonpath`: incorpora `src` durante la ejecución de pytest.
- `addopts`: muestra un resumen adicional de resultados.

```powershell
pytest
pytest tests/models/jugadas/test_jugada.py
```

## 16. Configuración de Ruff

```toml
[tool.ruff]
target-version = "py314"
line-length = 88
src = ["src", "tests"]
```

```powershell
ruff check .
```

## 17. Configuración de mypy

```toml
[tool.mypy]
python_version = "3.14"
strict = true
mypy_path = "src"
```

```powershell
mypy src
```

El modo estricto comprueba tanto anotaciones ausentes como usos incompatibles
de los tipos declarados.

## 18. Preparación del entorno virtual

Crear y activar el entorno en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar el proyecto:

```powershell
python -m pip install -e ".[dev]"
```

No deben editarse ni copiarse manualmente los archivos internos de `.venv`. El
entorno debe poder reconstruirse a partir de `pyproject.toml`.

## 19. Verificación

Comprobar el intérprete activo:

```powershell
python -c "import sys; print(sys.executable)"
```

Debe apuntar a:

```text
.venv\Scripts\python.exe
```

Comprobar la instalación del paquete:

```powershell
python -c "import piedra_papel_tijeras; print(piedra_papel_tijeras.__file__)"
```

Comprobar el registro editable y las dependencias:

```powershell
python -m pip list
```

Ejecutar las comprobaciones del proyecto:

```powershell
pytest
ruff check .
mypy src
```

## 20. Evolución versionada

La versión de `pyproject.toml` identifica el paquete instalado. Una etiqueta Git
identifica una versión concreta publicada en el historial del repositorio.

La evolución principal es:

```text
0.x     → construcción y consolidación del dominio
1.0.0   → primera aplicación CLI funcional
2.0.0   → aplicación gráfica PySide6
```

Actualmente `2.0.0` está declarada en `pyproject.toml`, pero todavía no existe
la etiqueta Git `v2.0.0`.

Antes de publicar una versión deben sincronizarse:

```text
pyproject.toml
README.md
documentación técnica
etiqueta Git
```

## 21. Criterio SemVer

```text
MAYOR.MENOR.PARCHE
```

- `MAYOR`: cambios principales o incompatibles en el contrato de uso.
- `MENOR`: funcionalidad compatible añadida.
- `PARCHE`: correcciones y refinamientos compatibles.

Antes de `1.0.0`, el proyecto se consideraba inestable. El salto a `1.0.0`
identificó la primera aplicación completa por consola. El paso a `2.0.0`
representa la sustitución de la interfaz principal por una GUI dirigida por
eventos, conservando el dominio anterior.

## 22. Mantenimiento

`pyproject.toml` no necesita cambiar con cada commit. Debe revisarse cuando
cambien:

| Cambio | Sección afectada |
| --- | --- |
| Nueva publicación | `project.version` |
| Metadatos del programa | `project` |
| Dependencia de ejecución | `project.dependencies` |
| Herramienta de desarrollo | `project.optional-dependencies` |
| Versiones admitidas de Python | `requires-python` |
| Comando de inicio | `project.scripts` |
| Estructura de paquetes | `tool.setuptools.packages.find` |
| Recursos distribuidos | `tool.setuptools.package-data` |
| Comportamiento de pruebas | `tool.pytest` |
| Reglas de análisis | `tool.ruff` o `tool.mypy` |

## 23. Resolución de problemas

### No se encuentra el paquete

```text
ModuleNotFoundError: No module named 'piedra_papel_tijeras'
```

Activar el entorno y reinstalar:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

### No se reconoce pytest

```powershell
python -m pytest
```

Si el módulo no existe, comprobar que se instaló el grupo `dev`.

### VS Code subraya los imports

Seleccionar el intérprete del entorno:

```text
Python: Select Interpreter
→ .venv\Scripts\python.exe
```

Después, reiniciar el servidor de lenguaje.

### Cambió `pyproject.toml`, pero el entorno conserva la configuración anterior

Repetir la instalación editable:

```powershell
python -m pip install -e ".[dev]"
```

## 24. Referencias

- [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Configuración de setuptools](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
- [Estructura `src-layout`](https://setuptools.pypa.io/en/stable/userguide/package_discovery.html)
- [Configuración de pytest](https://docs.pytest.org/en/stable/reference/customize.html)
