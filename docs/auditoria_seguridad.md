# Guía de auditoría y publicación segura del ejecutable

## 1. Propósito

Esta guía define el procedimiento para construir, auditar y distribuir de forma
controlada el ejecutable de **Piedra, Papel o Tijeras**.

Los controles se organizan en siete módulos:

1. Auditoría de vulnerabilidades de dependencias.
2. Construcción aislada o reproducible.
3. Comprobación del contenido de PyInstaller.
4. Generación del SBOM.
5. Análisis antivirus.
6. Firma digital.
7. Hash de publicación.

> Estos controles reducen riesgos y aportan evidencias, pero no garantizan una
> seguridad absoluta.

## 2. Orden de ejecución

```text
AUDITAR dependencias
        ↓
PREPARAR entorno aislado
        ↓
CONSTRUIR ejecutable
        ↓
INSPECCIONAR contenido
        ↓
GENERAR SBOM
        ↓
ANALIZAR con antivirus
        ↓
FIRMAR ejecutable
        ↓
CALCULAR hash definitivo
        ↓
PUBLICAR
```

La firma y el hash deben aplicarse al ejecutable definitivo. Cualquier
modificación posterior invalida el hash y puede invalidar la firma.

# Módulo 1 — Auditoría de vulnerabilidades de dependencias

## Objetivo

Identificar dependencias vulnerables, inesperadas, desactualizadas o procedentes
de fuentes no confiables antes de compilar el ejecutable.

## Riesgos controlados

- Dependencias con vulnerabilidades conocidas.
- Paquetes instalados accidentalmente.
- Diferencias entre `pyproject.toml` y el entorno real.
- Dependencias transitivas no identificadas.
- Paquetes manipulados o descargados desde una fuente incorrecta.

## Paso 1 — Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
```

El resultado debe apuntar a `.venv`.

## Paso 2 — Inventariar paquetes instalados

```powershell
python -m pip list
python -m pip freeze
```

Revisar que no aparezcan librerías ajenas al proyecto.

## Paso 3 — Comparar con `pyproject.toml`

La dependencia principal autorizada es PySide6. Las dependencias de desarrollo
son PyInstaller, pytest, Ruff y Mypy. También aparecerán componentes transitivos
legítimos de PySide6 y PyInstaller.

Todo paquete inesperado debe investigarse antes de compilar.

## Paso 4 — Auditar vulnerabilidades

La herramienta recomendada es `pip-audit`. Si está instalada:

```powershell
python -m pip_audit --local
```

## Paso 5 — Registrar resultados

| Campo         | Contenido                                    |
| ------------- | -------------------------------------------- |
| Paquete       | Componente afectado                          |
| Versión       | Versión instalada                            |
| Identificador | CVE o aviso                                  |
| Severidad     | Baja, media, alta o crítica                  |
| Exposición    | Si el proyecto utiliza la función vulnerable |
| Corrección    | Versión que resuelve el problema             |
| Decisión      | Actualizar, mitigar o aceptar                |

## Criterio de aprobación

- No existen vulnerabilidades críticas o altas sin resolver.
- Los paquetes instalados están justificados.
- Las versiones reales coinciden con las declaradas.
- No existen dependencias procedentes de fuentes desconocidas.

# Módulo 2 — Construcción aislada o reproducible

## Objetivo

Generar el ejecutable desde un entorno limpio, controlado y separado del entorno
habitual de desarrollo.

## Riesgos controlados

- Incorporación accidental de paquetes.
- Contaminación del entorno virtual.
- Uso de herramientas distintas entre compilaciones.
- Dependencia de configuraciones locales desconocidas.
- Compilación desde un equipo comprometido.

## Paso 1 — Seleccionar una versión concreta

La construcción debe partir de un commit conocido, una etiqueta Git estable y
un árbol de trabajo sin cambios inesperados:

```powershell
git status --short
git rev-parse HEAD
git describe --tags --exact-match
```

## Paso 2 — Crear un entorno limpio

Se recomienda crear un entorno específico para la construcción, separado de
`.venv`:

```powershell
python -m venv <entorno-de-construccion>
```

La creación del entorno requiere autorización porque modifica el sistema de
archivos.

## Paso 3 — Instalar únicamente dependencias autorizadas

Dentro del entorno limpio:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip freeze
```

El inventario debe conservarse como evidencia.

## Paso 4 — Ejecutar controles de calidad

```powershell
pytest
ruff check .
mypy src
```

No se debe compilar si fallan pruebas relacionadas con el comportamiento o la
integridad del proyecto.

## Paso 5 — Construir con una configuración oficial

Debe existir un único archivo `.spec` autorizado:

```powershell
pyinstaller --clean --noconfirm piedra_papel_tijeras.spec
```

## Paso 6 — Registrar el entorno

Registrar la versión de Windows, arquitectura, Python, pip, PyInstaller, commit
Git, dependencias, fecha y comando utilizado.

## Construcción reproducible

Con PyInstaller puede haber diferencias por marcas temporales, rutas internas,
metadatos PE, orden de componentes, firma digital o versión del sistema
operativo. El objetivo inicial será una construcción **aislada y repetible**. La
identidad byte a byte se tratará como un control adicional.

## Criterio de aprobación

- Entorno creado expresamente para la compilación.
- Solo contiene dependencias autorizadas.
- Pruebas y controles superados.
- Configuración y versiones registradas.
- Ejecutable generado desde un commit identificado.

# Módulo 3 — Comprobación del contenido de PyInstaller

## Objetivo

Verificar que PyInstaller ha incorporado exclusivamente código, bibliotecas y
recursos necesarios.

## Riesgos controlados

- DLL inesperadas.
- Hooks maliciosos.
- Paquetes residuales.
- Recursos no autorizados.
- Módulos de red o administración innecesarios.
- Ejecutables secundarios.

## Paso 1 — Revisar el archivo `.spec`

Comprobar `binaries`, `datas`, `hiddenimports`, `hookspath`, `runtime_hooks`,
`excludes`, `upx`, `runtime_tmpdir` y `console`.

Valores esperados:

- `binaries`: vacío salvo justificación.
- `hiddenimports`: vacío salvo necesidad comprobada.
- `hookspath`: vacío.
- `runtime_hooks`: vacío.
- `datas`: solamente recursos autorizados.
- `runtime_tmpdir`: sin ruta insegura.
- `console`: desactivado en la versión gráfica.

## Paso 2 — Revisar los avisos de construcción

Buscar dentro de `build/`:

```text
warn-*.txt
xref-*.html
Analysis-*.toc
PYZ-*.toc
PKG-*.toc
EXE-*.toc
```

Los avisos deben revisarse, no ignorarse automáticamente.

## Paso 3 — Inspeccionar el archivo ejecutable

```powershell
pyi-archive_viewer .\dist\piedra_papel_tijeras.exe
```

Debe comprobarse la presencia del paquete del proyecto, PySide6, componentes Qt
necesarios, Python y los nueve recursos PNG autorizados.

## Paso 4 — Buscar elementos inesperados

Revisar especialmente módulos como `subprocess`, `socket`, `requests`, `urllib`,
`ftplib`, `smtplib`, `winreg` y `ctypes`; comandos como PowerShell o `cmd.exe`;
ejecutables secundarios, certificados privados y archivos `.env`.

Algunas bibliotecas estándar pueden incorporarse indirectamente sin que el
proyecto las utilice. Su presencia debe evaluarse dentro del contexto.

## Paso 5 — Comparar con una lista permitida

La lista base debe contener módulos propios, dependencias autorizadas, DLL de
Python, DLL y plugins de Qt, recursos PNG y el bootloader de PyInstaller. Todo
elemento fuera de la lista requiere explicación.

## Criterio de aprobación

- No existen ejecutables secundarios inesperados.
- No se incorporan secretos.
- No existen hooks o scripts desconocidos.
- Los recursos coinciden con los autorizados.
- Las DLL y módulos adicionales están justificados.

# Módulo 4 — SBOM del ejecutable

## Objetivo

Crear un inventario estructurado de los componentes utilizados para generar el
ejecutable.

## Formato recomendado

Se recomienda **CycloneDX JSON**. Como alternativa puede utilizarse SPDX JSON.

## Contenido mínimo

- Aplicación y versión.
- Python, PySide6 y PyInstaller.
- Dependencias transitivas.
- Licencias disponibles.
- Identificadores, versiones y hashes.
- Relación entre componentes.

## Paso 1 — Generar el inventario del entorno

Ejemplo conceptual con una herramienta compatible con CycloneDX:

```powershell
cyclonedx-py environment --output-format JSON --output-file sbom.cdx.json
```

La sintaxis exacta debe comprobarse con la versión instalada.

## Paso 2 — Añadir metadatos de construcción

Registrar nombre, versión, commit, sistema operativo, Python, PyInstaller, fecha
de construcción y hash del ejecutable. El hash definitivo se añade después de
la firma.

## Paso 3 — Validar el SBOM

- El JSON debe ser válido.
- Las dependencias principales deben aparecer.
- No debe haber paquetes desconocidos.
- Las versiones deben coincidir con el entorno.
- El SBOM debe corresponder a la versión publicada.

## Paso 4 — Conservarlo junto a la versión

Archivar conjuntamente el ejecutable, SHA-256, versión, commit, firma e informe
de auditoría.

## Limitación

Un SBOM describe componentes, pero no demuestra que el binario esté libre de
malware.

## Criterio de aprobación

- Inventario completo y formato válido.
- Versiones verificadas.
- Correspondencia con la compilación definitiva.

# Módulo 5 — Análisis antivirus

## Objetivo

Detectar contenido malicioso conocido, comportamiento sospechoso o falsos
positivos antes de distribuir el ejecutable.

## Nivel 1 — Microsoft Defender

```powershell
Get-MpComputerStatus
Start-MpScan -ScanType CustomScan -ScanPath "<ruta-del-ejecutable>"
```

Estas operaciones pueden requerir permisos o autorización del sistema.

## Nivel 2 — Segundo motor

Utilizar un segundo antivirus independiente aumenta la cobertura. La ausencia de
detecciones no significa seguridad absoluta.

## Nivel 3 — Servicio multivirus

Antes de subir el archivo debe considerarse que puede compartirse con fabricantes
de seguridad y dejar de ser privado. La subida requiere autorización expresa.

## Nivel 4 — Análisis dinámico

Ejecutar el `.exe` en Windows Sandbox, una máquina virtual limpia o un equipo de
pruebas aislado. Observar procesos, archivos, registro, conexiones, persistencia,
procesos residuales y privilegios.

Comportamiento esperado:

```text
Abrir ventana
Leer clics
Cargar recursos locales
Mostrar resultados
Cerrar sin persistencia
No conectarse a Internet
No modificar archivos del usuario
```

## Falsos positivos

PyInstaller y UPX pueden provocar detecciones heurísticas. Ante una detección:

1. No ignorarla automáticamente.
2. Identificar el motor y la firma.
3. Repetir la compilación sin UPX.
4. Comparar resultados.
5. Inspeccionar el binario.
6. Solicitar revisión al fabricante cuando corresponda.

## Criterio de aprobación

- Sin detecciones confirmadas.
- Falsos positivos documentados.
- Sin conexiones de red, persistencia o escritura inesperada.
- Sin solicitud de administrador.

# Módulo 6 — Verificación y aplicación de firma digital

## Objetivo

Acreditar la identidad del editor y detectar modificaciones posteriores del
ejecutable mediante Authenticode, el sistema de firma de software de Windows.

La firma representa una declaración criptográfica:

```text
El titular de este certificado aprobó este archivo concreto
y el archivo no ha cambiado desde que fue firmado.
```

La firma no certifica que el programa sea seguro, que no tenga errores o que no
sea malware. Por eso debe aplicarse después de auditar, construir e inspeccionar
el ejecutable.

## Qué se utiliza y cuánto cuesta

```text
SignTool             Herramienta de Microsoft para firmar y verificar
Windows SDK          Paquete que proporciona SignTool
Certificado          Identifica al editor y da acceso a la clave privada
Servidor de tiempo   Confirma cuándo se realizó la firma
```

SignTool y Windows SDK son gratuitos. Un certificado autofirmado también puede
crearse gratuitamente, pero Windows no confiará en él de forma automática.

Para distribuir públicamente se recomienda un certificado específico de firma de
código emitido por una autoridad de certificación reconocida. Este certificado
normalmente es de pago y debe autorizar el uso:

```text
Code Signing
OID 1.3.6.1.5.5.7.3.3
```

## Impacto de la firma

| Aspecto         | Sin firma               | Con Authenticode válido                           |
| --------------- | ----------------------- | ------------------------------------------------- |
| Editor          | Desconocido             | Windows muestra al titular                        |
| Integridad      | No acreditada           | Cualquier alteración invalida la firma            |
| SmartScreen     | Menor confianza inicial | Mejora la identificación, no garantiza reputación |
| Antivirus       | Archivo anónimo         | Archivo atribuible, pero sigue siendo analizado   |
| Responsabilidad | Difícil atribución      | El titular queda vinculado al binario             |
| Distribución    | Advertencias frecuentes | Presentación más profesional y verificable        |

Firmar modifica físicamente el `.exe`. Por ello, el hash SHA-256 de publicación
debe calcularse después de firmar.

## Paso 1 — Verificar el estado actual

```powershell
Get-AuthenticodeSignature ".\dist\piedra_papel_tijeras.exe"
```

| Estado         | Significado                            |
| -------------- | -------------------------------------- |
| `Valid`        | Firma válida                           |
| `NotSigned`    | Archivo sin firma                      |
| `HashMismatch` | Archivo modificado después de firmarse |
| `NotTrusted`   | Certificado no confiable               |
| `UnknownError` | No se pudo validar                     |

## Paso 2 — Obtener un certificado

Para distribución pública se necesita un certificado de firma de código emitido
por una autoridad confiable. Para pruebas internas se puede utilizar un
certificado autofirmado exclusivo, sabiendo que otros equipos no confiarán en él
salvo que instalen expresamente su certificado raíz.

Antes de firmar debe comprobarse:

```text
El certificado permite Code Signing
El certificado está vigente y no revocado
El titular tiene acceso a su clave privada
La clave no se encuentra dentro del proyecto
El ejecutable definitivo ya pasó auditoría y antivirus
```

La clave privada no debe guardarse en Git, enviarse por correo ni copiarse junto
al ejecutable. Si se utiliza un archivo `.pfx`, debe protegerse con contraseña y
almacenarse fuera del repositorio. No debe escribirse su contraseña directamente
en scripts o documentación.

## Paso 3 — Firmar con Authenticode

### 3.1 Localizar SignTool

SignTool se distribuye gratuitamente dentro de Windows SDK. Que el comando no
responda no significa necesariamente que falte: puede estar instalado sin que su
directorio figure en `PATH`.

#### 3.1.1 Comprobar si está disponible mediante PATH

```powershell
Get-Command signtool -ErrorAction SilentlyContinue
```

```text
Muestra CommandType, Name y Source
    → SignTool está disponible.

No muestra resultados
    → Debe buscarse su archivo antes de instalar nada.
```

#### 3.1.2 Buscar una instalación existente

Microsoft suele instalarlo en una ruta con esta estructura:

```text
C:\Program Files (x86)\Windows Kits\10\bin\<versión>\x64\signtool.exe
```

La siguiente comprobación es de solo lectura y selecciona la versión x64 más
reciente encontrada:

```powershell
$signTool = Get-ChildItem `
    "${env:ProgramFiles(x86)}\Windows Kits\10\bin" `
    -Filter "signtool.exe" `
    -File `
    -Recurse `
    -ErrorAction SilentlyContinue |
    Where-Object FullName -Match "\\x64\\signtool\.exe$" |
    Sort-Object FullName -Descending |
    Select-Object -First 1

$signTool
```

```text
Muestra una ruta
    → SignTool ya está instalado.

No muestra resultados
    → Probablemente falta Windows SDK o su componente de firma.
```

#### 3.1.3 Probar la herramienta mediante su ruta completa

Si la búsqueda encontró el archivo:

```powershell
& $signTool.FullName /?
```

La ayuda debe mostrar operaciones como:

```text
sign
verify
timestamp
remove
```

No es necesario añadir SignTool permanentemente a `PATH`. Utilizar su ruta
completa evita modificar la configuración del sistema.

#### 3.1.4 Instalar Windows SDK si realmente falta

La instalación modifica el equipo y requiere autorización previa. Debe utilizarse
exclusivamente el instalador oficial de Microsoft:

1. Abrir `https://developer.microsoft.com/windows/downloads/windows-sdk/`.
2. Descargar el instalador de Windows SDK.
3. Comprobar que Windows identifica al editor como `Microsoft Corporation`.
4. Ejecutar el instalador con permisos administrativos.
5. Seleccionar las herramientas de firma para aplicaciones de escritorio cuando
   el instalador permita elegir componentes.
6. Completar la instalación.
7. Cerrar y abrir una nueva terminal PowerShell.
8. Repetir los pasos 3.1.1 y 3.1.2.

Si Visual Studio ya está instalado, puede añadirse el SDK mediante:

```text
Menú Inicio
→ Visual Studio Installer
→ Modificar
→ Componentes individuales
→ Windows SDK
→ Modificar o instalar
```

No es necesario instalar el entorno completo de Visual Studio únicamente para
obtener SignTool; Windows SDK es suficiente.

#### 3.1.5 Verificar procedencia, arquitectura y versión

Para firmar el ejecutable Windows de 64 bits se utilizará preferentemente la
variante situada en `x64`:

```powershell
$signTool.FullName
$signTool.VersionInfo |
    Select-Object FileVersion, ProductVersion, CompanyName
```

El resultado esperado debe identificar:

```text
CompanyName: Microsoft Corporation
```

Si el editor o la ruta no son los esperados, no debe ejecutarse la herramienta
hasta investigar su procedencia.

#### 3.1.6 Preparar la ruta para los pasos siguientes

```powershell
$signToolPath = $signTool.FullName
```

Se utilizará de esta forma:

```powershell
& $signToolPath sign <opciones> <ejecutable>
& $signToolPath verify <opciones> <ejecutable>
```

La variable solo existe en la sesión actual de PowerShell. No instala nada ni
modifica permanentemente Windows.

### 3.2 Identificar el certificado

Es preferible seleccionar expresamente el certificado de firma de código. No se
recomienda `/a` en un equipo que contenga varios certificados, porque permite que
SignTool elija uno automáticamente.

Puede comprobarse qué certificados del usuario permiten firma de código:

```powershell
Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert |
    Select-Object Subject, Thumbprint, NotAfter, HasPrivateKey
```

La huella y los datos personales no deben publicarse sin necesidad.

### 3.3 Firmar desde el almacén de certificados

Plantilla orientativa:

```powershell
signtool sign `
    /fd SHA256 `
    /sha1 "<HUELLA_DEL_CERTIFICADO>" `
    /tr "<SERVIDOR_RFC3161_DEL_PROVEEDOR>" `
    /td SHA256 `
    /d "Piedra, Papel o Tijeras" `
    ".\dist\piedra_papel_tijeras.exe"
```

```text
/fd SHA256   Firma el hash del ejecutable con SHA-256
/sha1        Selecciona el certificado mediante su huella
/tr          Solicita un sello de tiempo RFC 3161
/td SHA256   Usa SHA-256 para el sello de tiempo
/d           Añade una descripción legible del programa
```

`/sha1` solo identifica el certificado por su huella; el ejecutable sigue
firmándose mediante SHA-256.

### 3.4 Firmar mediante un archivo PFX

Solo cuando el proveedor entregue un `.pfx` y no exista una opción más protegida:

```powershell
signtool sign `
    /fd SHA256 `
    /f "<RUTA_PROTEGIDA_AL_CERTIFICADO.pfx>" `
    /tr "<SERVIDOR_RFC3161_DEL_PROVEEDOR>" `
    /td SHA256 `
    ".\dist\piedra_papel_tijeras.exe"
```

No debe añadirse `/p <contraseña>` a un script permanente, porque la contraseña
podría quedar en el historial, registros o repositorio. Debe seguirse el método
seguro indicado por el proveedor del certificado.

## Paso 4 — Aplicar sello de tiempo

El sello de tiempo no es una segunda firma del autor. Es la confirmación de un
tercero de que el archivo fue firmado en una fecha determinada:

```text
Firma sin sello de tiempo
    El certificado caduca → la validez futura puede verse afectada

Firma con sello de tiempo
    El certificado caduca → puede demostrarse que se firmó durante su vigencia
```

Debe utilizarse el servidor RFC 3161 indicado por el proveedor del certificado.
Muchos proveedores incluyen el servicio de sellado con el certificado, pero sus
condiciones deben comprobarse.

## Paso 5 — Verificar después de firmar

```powershell
Get-AuthenticodeSignature ".\dist\piedra_papel_tijeras.exe" |
    Format-List Status, StatusMessage, SignerCertificate, TimeStamperCertificate

signtool verify /pa /v ".\dist\piedra_papel_tijeras.exe"
```

```text
/pa   Aplica la política normal de verificación Authenticode
/v    Muestra información detallada
```

El resultado esperado es `Valid` y la identificación correcta del firmante y
del servidor de tiempo. No debe publicarse si aparece `HashMismatch`,
`NotTrusted`, `UnknownError` o una advertencia sin investigar.

## Paso 6 — Proteger el ejecutable firmado

Después de firmarlo no debe modificarse, comprimirse, editarse ni reconstruirse
conservando el mismo hash. El flujo final es:

```text
FIRMAR ejecutable
        ↓
VERIFICAR firma y sello de tiempo
        ↓
REPETIR análisis antivirus
        ↓
CALCULAR SHA-256 definitivo
        ↓
PUBLICAR ejecutable y hash
```

Si se recompila o se cambia el icono, los recursos o los metadatos, debe repetirse
todo el proceso desde la firma.

## Impacto si la clave privada se compromete

Quien obtenga la clave privada podría firmar software haciéndose pasar por el
titular. Ante una sospecha de compromiso debe detenerse la publicación, revocar
el certificado, avisar al proveedor y conservar evidencias de qué versiones se
firmaron legítimamente.

## Criterio de aprobación

- Estado de firma `Valid`.
- Certificado autorizado específicamente para Code Signing.
- Certificado correspondiente al editor.
- Sello de tiempo válido.
- Archivo no modificado después de la firma.
- Clave privada almacenada fuera del repositorio.
- Análisis antivirus repetido tras la firma.
- Hash SHA-256 calculado sobre el archivo firmado.

# Módulo 7 — Hash de publicación

## Objetivo

Permitir que cualquier destinatario compruebe que el archivo recibido coincide
exactamente con el publicado.

## Algoritmo

Utilizar SHA-256. No utilizar MD5 o SHA-1 para este propósito.

## Paso 1 — Calcular el hash definitivo

Debe calcularse después de la construcción, inspección, firma, último análisis y
cualquier modificación:

```powershell
Get-FileHash "<ruta-del-ejecutable>" -Algorithm SHA256
```

## Paso 2 — Registrar la versión

```text
SHA256  nombre-del-archivo  versión  commit
```

## Paso 3 — Publicar mediante un canal confiable

Publicar el hash en la página oficial de la versión, el repositorio, una página
servida mediante HTTPS o un archivo firmado.

## Paso 4 — Verificación del usuario

```powershell
Get-FileHash ".\piedra_papel_tijeras.exe" -Algorithm SHA256
```

El resultado debe coincidir exactamente con el publicado.

## Paso 5 — Recalcular ante cualquier cambio

La firma, el cambio de icono, la recompilación, los recursos, las dependencias y
los metadatos alteran el hash. Cada archivo diferente necesita su propio hash.

## Criterio de aprobación

- Hash calculado sobre el binario firmado definitivo.
- Hash publicado mediante un canal confiable.
- Nombre y versión identificados.
- Coincidencia verificada antes de distribuir.

# Lista final de publicación

## Dependencias

- [x] Dependencias inventariadas.
- [x] Vulnerabilidades auditadas.
- [x] Paquetes inesperados investigados.
- [x] Versiones registradas.

## Construcción

- [x] Commit identificado.
- [x] Entorno limpio.
- [ ] Pruebas, Ruff y Mypy superados.
- [ ] Configuración `.spec` oficial.
- [ ] Registro de construcción conservado.

## Contenido

- [ ] Recursos autorizados.
- [ ] Sin secretos ni hooks inesperados.
- [ ] Sin ejecutables secundarios.
- [ ] DLL y módulos justificados.

## Trazabilidad

- [ ] SBOM generado y validado.
- [ ] Versión y commit asociados.

## Seguridad del binario

- [ ] Microsoft Defender sin detecciones confirmadas.
- [ ] Segundo análisis realizado.
- [ ] Prueba en entorno limpio.
- [ ] Sin red, persistencia ni privilegios inesperados.

## Publicación

- [ ] Firma Authenticode válida.
- [ ] Sello de tiempo válido.
- [ ] SHA-256 definitivo calculado y publicado.
- [ ] Ejecutable final verificado.

# Criterio general de detención

La publicación debe detenerse ante cualquiera de estas situaciones:

- Vulnerabilidad crítica o alta sin evaluar.
- Dependencia desconocida.
- Detección antivirus no explicada.
- Conexión de red, escritura o persistencia no prevista.
- Firma inválida.
- Diferencia entre el hash calculado y el publicado.
- Contenido inesperado dentro del ejecutable.
- Compilación realizada desde un entorno comprometido.
- Imposibilidad de relacionar el ejecutable con un commit concreto.

# Resultado esperado

Al completar los siete módulos se dispondrá de:

```text
Código fuente identificado
Dependencias auditadas
Entorno de construcción controlado
Ejecutable inspeccionado
SBOM
Resultados antivirus
Firma digital verificable
Hash SHA-256 público
Trazabilidad entre versión, código y binario
```

Esto proporciona una base sólida para distribuir el ejecutable con un nivel de
confianza considerablemente superior.
