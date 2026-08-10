# Pruebas y calidad

Este directorio reúne las pruebas automatizadas de los componentes actualmente
implementados: tipos, resultados, jugadas, jugadores, partida e interfaz de
consola.

## Arquitectura actual de pruebas

| Archivo                                   | Responsabilidad                                     |
| ----------------------------------------- | --------------------------------------------------- |
| `models/jugadas/test_jugada.py`           | Contrato común y comportamiento base de `Jugada`.   |
| `models/jugadas/test_fabrica_jugadas.py`  | Creación de jugadas y validación del tipo recibido. |
| `models/jugadas/test_piedra.py`           | Comportamiento específico de `Piedra`.              |
| `models/jugadas/test_papel.py`            | Comportamiento específico de `Papel`.               |
| `models/jugadas/test_tijeras.py`          | Comportamiento específico de `Tijeras`.             |
| `models/jugadores/test_jugador_humano.py` | Selección y creación de jugadas del jugador humano. |
| `models/jugadores/test_jugador_maquina.py` | Selección aleatoria de jugadas de la máquina.        |
| `models/test_resultado.py`                 | Valores y representación de los resultados.         |
| `models/test_tipo_jugada.py`              | Valores y representación textual de `TipoJugada`.   |
| `services/test_partida.py`                | Resolución de victoria, derrota y empate.            |
| `test_main.py`                            | Validación de entrada y ejecución de la CLI.         |

## Convenciones generales

- Cada prueba debe verificar un único comportamiento.
- Los nombres deben seguir el patrón `test_<condicion>_<resultado_esperado>`.
- Las pruebas deben ser independientes y no compartir estado mutable.
- El resultado no debe depender del orden de ejecución.
- Los casos equivalentes deben agruparse mediante parametrización con pytest.
- Cada nuevo componente debe disponer de un archivo `test_<componente>.py`.
- Las pruebas deben centrarse en el comportamiento observable.

## Ejecución

La configuración de pytest está centralizada en `pyproject.toml`. Después de
instalar el proyecto y las dependencias de desarrollo:

```powershell
python -m pip install -e ".[dev]"
```

puede ejecutarse toda la batería:

```powershell
pytest
```

O un módulo concreto:

```powershell
pytest tests/models/jugadas/test_jugada.py
```

La instalación editable y la propiedad `pythonpath = ["src"]` permiten importar
`piedra_papel_tijeras` sin configurar `PYTHONPATH` manualmente.

## Estado de la cobertura funcional

Las casillas marcadas representan pruebas presentes en la batería actual. Las
casillas pendientes señalan comportamientos implementados que todavía no están
cubiertos por una prueba.

### `test_jugada.py`

- [x] `Jugada` no puede instanciarse directamente por ser una clase abstracta.
- [x] `vence_a()` devuelve `True` cuando la jugada vence a la recibida.
- [x] `vence_a()` devuelve `False` ante una derrota o un empate.
- [x] `vence_a()` rechaza valores que no sean instancias de `Jugada`.
- [x] La representación textual de una jugada coincide con su tipo.

### `test_fabrica_jugadas.py`

- [x] `TipoJugada.PIEDRA` produce una instancia de `Piedra`.
- [x] `TipoJugada.PAPEL` produce una instancia de `Papel`.
- [x] `TipoJugada.TIJERAS` produce una instancia de `Tijeras`.
- [x] La fábrica rechaza valores que no sean instancias de `TipoJugada`.

### `test_tipo_jugada.py`

- [x] El enumerado define los tipos piedra, papel y tijeras.
- [x] Cada tipo conserva el valor textual esperado.
- [x] La conversión a texto devuelve el valor de la jugada.

### Batería común de jugadas concretas

Estos casos corresponden a `test_piedra.py`, `test_papel.py` y
`test_tijeras.py`.

- [x] Cada clase puede instanciarse correctamente.
- [x] Cada instancia expone su `tipo` y `nombre` correspondientes.
- [x] Cada jugada vence a la jugada definida por sus reglas.
- [x] Cada jugada pierde frente a la jugada correspondiente.
- [x] Cada jugada empata con otra instancia del mismo tipo.

#### `test_piedra.py`

- [x] Piedra vence a tijeras.
- [x] Piedra pierde frente a papel.
- [x] Piedra empata con piedra.

#### `test_papel.py`

- [x] Papel vence a piedra.
- [x] Papel pierde frente a tijeras.
- [x] Papel empata con papel.

#### `test_tijeras.py`

- [x] Tijeras vence a papel.
- [x] Tijeras pierde frente a piedra.
- [x] Tijeras empata con tijeras.

### `test_jugador_humano.py`

- [x] Conserva el nombre recibido al construir el jugador.
- [x] El método `__str__` devuelve la cadena correcta
- [x] Convierte piedra, papel y tijeras en su `TipoJugada` correspondiente.
- [x] Acepta diferencias de mayúsculas y espacios exteriores.
- [x] Rechaza una entrada inválida y vuelve a solicitarla.
- [x] Tras una entrada inválida, devuelve el tipo correspondiente a la siguiente
      entrada válida.
- [x] `elegir_jugada()` devuelve la `Jugada` concreta correspondiente a la
      selección.

### `test_jugador_maquina.py`

- [x] Conserva el nombre predeterminado.
- [x] Conserva un nombre personalizado.
- [x] El método `__str__` devuelve la cadena correcta.
- [x] `_seleccionar_tipo()` utiliza el generador inyectado.
- [x] El generador recibe exclusivamente los miembros de `TipoJugada`.
- [x] `elegir_jugada()` devuelve `Piedra`, `Papel` o `Tijeras` según el tipo
      seleccionado.

### `test_resultado.py`

- [x] Cada resultado conserva su valor y representación textual.

### `test_partida.py`

- [x] Resuelve victoria, derrota y empate desde la perspectiva humana.

### `test_main.py`

- [x] Normaliza una entrada válida.
- [x] Repite la solicitud después de una entrada inválida.
- [x] Ejecuta una ronda completa y muestra su resultado.
