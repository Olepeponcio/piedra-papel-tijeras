# Pruebas y calidad

Este directorio reúne las pruebas automatizadas de los componentes actualmente
implementados: `TipoJugada`, la jerarquía de jugadas y su fábrica.

`Partida` y la interfaz de consola todavía no tienen lógica implementada, por lo
que sus pruebas se incorporarán cuando esos componentes estén disponibles.

## Arquitectura actual de pruebas

| Archivo                                    | Estado    | Responsabilidad                                      |
| ------------------------------------------ | --------- | ---------------------------------------------------- |
| `models/jugadas/test_jugada.py`          | Parcial   | Contrato común y comportamiento base de `Jugada`.    |
| `models/jugadas/test_fabrica_jugadas.py` | Cubierto  | Creación de jugadas y validación del tipo recibido.  |
| `models/jugadas/test_piedra.py`          | Pendiente | Comportamiento específico de `Piedra`.               |
| `models/jugadas/test_papel.py`           | Pendiente | Comportamiento específico de `Papel`.                |
| `models/jugadas/test_tijeras.py`         | Pendiente | Comportamiento específico de `Tijeras`.              |
| `models/test_tipo_jugada.py`             | Pendiente | Valores y representación textual de `TipoJugada`.    |

## Convenciones generales

- Cada prueba debe verificar un único comportamiento.
- Los nombres deben seguir el patrón `test_<condicion>_<resultado_esperado>`.
- Las pruebas deben ser independientes y no compartir estado mutable.
- El resultado no debe depender del orden de ejecución.
- Los casos equivalentes deben agruparse mediante parametrización con pytest.
- Cada nuevo componente debe disponer de un archivo `test_<componente>.py`.
- Las pruebas deben centrarse en el comportamiento observable.

## Ejecución

Desde el directorio raíz del proyecto:

```powershell
$env:PYTHONPATH="src"
pytest
```

La variable permite que Python encuentre el paquete `piedra_papel_tijeras`,
ubicado dentro de `src`. Debe establecerse de nuevo al abrir una sesión nueva de
PowerShell.

## Estado de la cobertura funcional

Las casillas marcadas representan pruebas presentes en la batería actual. Las
casillas pendientes señalan comportamientos implementados que todavía no están
cubiertos por una prueba.

### `test_jugada.py`

- [x] `Jugada` no puede instanciarse directamente por ser una clase abstracta.
- [ ] `vence_a()` devuelve `True` cuando la jugada vence a la recibida.
- [ ] `vence_a()` devuelve `False` ante una derrota o un empate.
- [ ] `vence_a()` rechaza valores que no sean instancias de `Jugada`.
- [ ] La representación textual de una jugada coincide con su tipo.

### `test_fabrica_jugadas.py`

- [x] `TipoJugada.PIEDRA` produce una instancia de `Piedra`.
- [x] `TipoJugada.PAPEL` produce una instancia de `Papel`.
- [x] `TipoJugada.TIJERAS` produce una instancia de `Tijeras`.
- [x] La fábrica rechaza valores que no sean instancias de `TipoJugada`.

### `test_tipo_jugada.py`

- [ ] El enumerado define los tipos piedra, papel y tijeras.
- [ ] Cada tipo conserva el valor textual esperado.
- [ ] La conversión a texto devuelve el valor de la jugada.

### Batería común de jugadas concretas

Estos casos corresponden a `test_piedra.py`, `test_papel.py` y
`test_tijeras.py`. Actualmente, los tres archivos están vacíos.

- [ ] Cada clase puede instanciarse correctamente.
- [ ] Cada instancia expone su `tipo` y `nombre` correspondientes.
- [ ] Cada jugada vence a la jugada definida por sus reglas.
- [ ] Cada jugada pierde frente a la jugada correspondiente.
- [ ] Cada jugada empata con otra instancia del mismo tipo.

#### `test_piedra.py`

- [ ] Piedra vence a tijeras.
- [ ] Piedra pierde frente a papel.
- [ ] Piedra empata con piedra.

#### `test_papel.py`

- [ ] Papel vence a piedra.
- [ ] Papel pierde frente a tijeras.
- [ ] Papel empata con papel.

#### `test_tijeras.py`

- [ ] Tijeras vence a papel.
- [ ] Tijeras pierde frente a piedra.
- [ ] Tijeras empata con tijeras.

## Componentes futuros

Las pruebas de `Partida`, jugadores y la interfaz de consola quedan fuera de la
batería actual porque esos componentes todavía no están implementados.
