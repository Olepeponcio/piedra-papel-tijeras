# Pruebas y calidad

Este directorio reúne las pruebas automatizadas del proyecto. Su finalidad es comprobar que las jugadas respetan las reglas de piedra, papel o tijeras y mantener un criterio común para las pruebas que se incorporen en el futuro.

## Pruebas actuales

La batería está distribuida según la responsabilidad evaluada:

| Archivo           | Responsabilidad                                                |
| ----------------- | -------------------------------------------------------------- |
| `test_jugada.py`  | Comprueba el contrato y el comportamiento común de una jugada. |
| `test_piedra.py`  | Comprueba las reglas específicas de piedra.                    |
| `test_papel.py`   | Comprueba las reglas específicas de papel.                     |
| `test_tijeras.py` | Comprueba las reglas específicas de tijeras.                   |

## Convenciones generales

- Cada prueba debe verificar un único comportamiento.
- Los nombres deben seguir el patrón `test_<condicion>_<resultado_esperado>`.
- Las pruebas deben ser independientes y no compartir estado mutable.
- El resultado no debe depender del orden de ejecución.
- Los casos equivalentes deben agruparse mediante parametrización con pytest.
- Cada nuevo componente debe disponer de un archivo de prueba con el patrón `test_<componente>.py`.
- Las pruebas deben centrarse en el comportamiento observable, no en detalles internos de implementación.

## Ejecución

Desde el directorio raíz del proyecto:

```bash
pytest
```

## Detalle de las pruebas

Las siguientes cuestiones definen los comportamientos que deberán comprobarse.

### `test_jugada.py`

Contrato y comportamiento común de una jugada:

- [ ] La clase debe representar una jugada válida.
- [ ] La clase debe definir cómo se compara con otra jugada.
- [ ] La comparación debe devolver un resultado coherente y predecible.
- [ ] La clase debe rechazar o gestionar una comparación con un valor no válido.

### Batería común para piedra, papel y tijeras

Los tres tipos de jugada comparten la misma batería de casos:

- [ ] La clase debe poder instanciarse correctamente.
- [ ] La jugada debe vencer a la jugada correspondiente.
- [ ] La jugada debe perder frente a la jugada correspondiente.
- [ ] La jugada debe empatar con otra instancia del mismo tipo.
- [ ] La comparación debe devolver un resultado coherente y predecible.

Los casos equivalentes deben parametrizarse para evitar repetir la misma lógica en distintos archivos.

### `test_piedra.py`

- [ ] Piedra debe vencer a tijeras.
- [ ] Piedra debe perder frente a papel.
- [ ] Piedra debe empatar con piedra.

### `test_papel.py`

- [ ] Papel debe vencer a piedra.
- [ ] Papel debe perder frente a tijeras.
- [ ] Papel debe empatar con papel.

### `test_tijeras.py`

- [ ] Tijeras debe vencer a papel.
- [ ] Tijeras debe perder frente a piedra.
- [ ] Tijeras debe empatar con tijeras.
