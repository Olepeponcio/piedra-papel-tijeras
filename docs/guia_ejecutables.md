# Guía para generar ejecutables

Esta guía describe cómo distribuir la aplicación gráfica Piedra, papel o tijeras,
desarrollada con PySide6, sin exigir que el usuario instale Python, PySide6 ni las
demás dependencias del proyecto.

## 1. Estado de la aplicación

La versión estable actual es `v2.0.0` y utiliza:

- PySide6 `6.11.1` para la interfaz gráfica.
- `QApplication` como ciclo principal de la aplicación.
- `VentanaDeJuego`, basada en `QMainWindow`, como ventana principal.
- Recursos PNG almacenados en `src/piedra_papel_tijeras/resources`.
- `src/piedra_papel_tijeras/main.py` como punto de entrada.

La función `main()` inicia actualmente la interfaz PySide6. La función
`main_consola()` se conserva como interfaz histórica, pero no constituye el punto
de entrada activo.

## 2. Alcance del ejecutable autónomo

PyInstaller incorpora el intérprete de Python, PySide6, los plugins Qt necesarios
y las dependencias detectadas en el artefacto generado. El usuario final no
necesita instalar esos componentes.

El modo `onefile` genera un único archivo distribuible. Al iniciarlo, PyInstaller
extrae internamente los componentes necesarios en un directorio temporal y
ejecuta la aplicación desde allí.

## 3. Compatibilidad por sistema operativo

PyInstaller no es un compilador cruzado:

- Una construcción realizada en Windows produce un `.exe` para Windows.
- Una construcción realizada en macOS produce un ejecutable o paquete para macOS.
- Una construcción realizada en Linux produce un ejecutable para Linux.

El `.exe` de Windows no funciona en macOS ni Linux. Para publicar en varios
sistemas se debe construir y probar un artefacto independiente dentro de cada
sistema operativo, mediante equipos físicos, máquinas virtuales o integración
continua.

## 4. Preparar el entorno de construcción en Windows

Desde la raíz del proyecto, crea y activa el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala el proyecto, PySide6 y las herramientas de desarrollo declaradas en
`pyproject.toml`:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Comprueba que se utilizan el intérprete y PyInstaller del entorno:

```powershell
python -c "import sys; print(sys.executable)"
pyinstaller --version
```

## 5. Validaciones previas

Antes de construir una versión distribuible:

```powershell
pytest
ruff check .
mypy src
```

La construcción debe partir del código de una versión estable. Para comprobar la
etiqueta actual:

```powershell
git describe --tags --exact-match
```

## 6. Generar el ejecutable PySide6 en un único archivo

Desde la raíz del proyecto:

```powershell
pyinstaller --clean --noconfirm --onefile --windowed --name piedra_papel_tijeras --paths src --add-data "src\piedra_papel_tijeras\resources:piedra_papel_tijeras\resources" src\piedra_papel_tijeras\main.py
```

Opciones utilizadas:

- `--clean`: limpia la caché de PyInstaller antes de construir.
- `--noconfirm`: sustituye una salida anterior sin pedir confirmación.
- `--onefile`: genera un único archivo ejecutable.
- `--windowed`: inicia la GUI sin abrir una consola adicional.
- `--name`: define el nombre del ejecutable y del archivo `.spec`.
- `--paths src`: añade `src` a las rutas donde se buscan imports.
- `--add-data`: incorpora los PNG respetando la ruta esperada por la GUI.

En PyInstaller 6.22.0, `--add-data` utiliza el formato `SOURCE:DEST` para separar
el origen y el destino interno.

## 7. Resultado de la construcción

PyInstaller genera:

```text
build/
dist/piedra_papel_tijeras.exe
piedra_papel_tijeras.spec
```

- `build/` contiene archivos temporales.
- `dist/` contiene el ejecutable distribuible.
- `piedra_papel_tijeras.spec` contiene la configuración reproducible.

Ejecuta el resultado con:

```powershell
.\dist\piedra_papel_tijeras.exe
```

## 8. Comprobar la interfaz y los recursos

La validación manual debe confirmar:

1. La ventana principal se abre sin consola adicional.
2. Los iconos de piedra, papel y tijeras aparecen en sus botones.
3. Al ejecutar una ronda aparecen las imágenes de ambas jugadas.
4. Se muestra la imagen correspondiente a victoria, derrota o empate.
5. La aplicación se cierra sin procesos residuales.

La GUI calcula el directorio de recursos desde `ventana_de_juego.py`:

```text
piedra_papel_tijeras/gui/ventana_de_juego.py
                              ↓
piedra_papel_tijeras/resources/
```

Por ese motivo, el destino interno de `--add-data` debe conservar exactamente
`piedra_papel_tijeras/resources`.

También debe probarse el `.exe` en otro equipo Windows que no tenga Python ni
PySide6 instalados.

## 9. Reutilizar el archivo `.spec`

Después de comprobar la primera construcción, el archivo
`piedra_papel_tijeras.spec` puede conservarse como configuración oficial. Las
construcciones posteriores se realizan con:

```powershell
pyinstaller --clean --noconfirm piedra_papel_tijeras.spec
```

El `.spec` almacena el punto de entrada, el modo de ventana, el nombre, las rutas
de búsqueda y los recursos. Cuando se construye desde él, no deben repetirse en
el comando opciones como `--onefile`, `--windowed` o `--add-data`.

Antes de versionar el `.spec`, se debe revisar que contenga:

- `src/piedra_papel_tijeras/main.py` como script de entrada.
- `src` dentro de `pathex`.
- Los PNG dentro de `datas` con destino
  `piedra_papel_tijeras/resources`.
- `console=False` en la configuración de `EXE`.
- `piedra_papel_tijeras` como nombre del ejecutable.

## 10. PySide6 y plugins Qt

PyInstaller incluye hooks específicos para detectar PySide6 y sus plugins Qt. En
una construcción normal no es recomendable añadir indiscriminadamente todo
PySide6, porque aumentaría el tamaño del ejecutable.

Si una compilación informa de un módulo o plugin ausente:

1. Revisar los avisos generados dentro de `build/`.
2. Identificar el import o plugin concreto.
3. Añadir solamente el `hiddenimport`, plugin o dato necesario al `.spec`.
4. Reconstruir y repetir la prueba en un equipo limpio.

## 11. Compilación de diagnóstico

Si la aplicación se cierra sin mostrar el error, puede generarse temporalmente
una versión con consola:

```powershell
pyinstaller --clean --noconfirm --onefile --console --name piedra_papel_tijeras_debug --paths src --add-data "src\piedra_papel_tijeras\resources:piedra_papel_tijeras\resources" src\piedra_papel_tijeras\main.py
```

Esta variante es únicamente para diagnóstico. La distribución gráfica estable
debe utilizar `--windowed` o `console=False`.

## 12. Limpieza

Después de validar el ejecutable:

- `build/` puede eliminarse porque solo contiene artefactos temporales.
- `dist/` contiene el binario que se distribuye.
- El `.spec` debe conservarse si es la configuración oficial.
- Las cachés y artefactos temporales no deben publicarse.

## 13. macOS y Linux

En cada sistema de destino se debe:

1. Crear un entorno virtual propio.
2. Instalar el proyecto con `python -m pip install -e ".[dev]"`.
3. Confirmar que las rutas de `--add-data` existen en ese sistema.
4. Ejecutar PyInstaller dentro de ese sistema.
5. Probar el artefacto en una instalación limpia compatible.

En Linux debe comprobarse la compatibilidad con la distribución y sus bibliotecas
base. En macOS deben considerarse la arquitectura, la firma de código y la
notarización para una distribución pública.

## 14. Política de versiones y publicación

- La versión estable actual está identificada por la etiqueta Git `v2.0.0`.
- Solo se publicará el ejecutable de la última versión estable.
- El ejecutable nuevo sustituirá al anterior.
- Los binarios históricos no se conservarán dentro del repositorio.
- Las etiquetas Git conservarán el historial del código fuente.
- `build/`, cachés y archivos temporales no se publicarán.

Actualmente `dist/` está excluido mediante `.gitignore`. Antes de incorporar el
ejecutable al repositorio se deberá añadir una excepción limitada al nombre y a
la ubicación del único binario autorizado.

## 15. Referencias oficiales

- [Manual de PyInstaller](https://pyinstaller.org/en/stable/)
- [Opciones y uso de PyInstaller](https://pyinstaller.org/en/stable/usage.html)
- [Uso de archivos spec](https://pyinstaller.org/en/latest/spec-files.html)
