import pytest
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


# El enumerado define los tipos piedra, papel y tijeras.
def test_clase_enum_define_tipos_piedra_papel_tijeras() -> None:
    assert set(TipoJugada) == {TipoJugada.PIEDRA, TipoJugada.PAPEL, TipoJugada.TIJERAS}


@pytest.mark.parametrize(
    ("tipo", "valor_esperado"),
    [
        (TipoJugada.PIEDRA, "Piedra"),
        (TipoJugada.TIJERAS, "Tijeras"),
        (TipoJugada.PAPEL, "Papel"),
    ],
)
# Cada tipo conserva el valor textual esperado.
def test_cada_tipo_conserva_valor_textual_esperado(
    tipo: TipoJugada, valor_esperado: str
) -> None:
    assert tipo.value == valor_esperado


@pytest.mark.parametrize(
    "tipo",
    [
        TipoJugada.PIEDRA,
        TipoJugada.PAPEL,
        TipoJugada.TIJERAS,
    ],
)
def test_conversion_a_texto_devuelve_valor_del_tipo(tipo: TipoJugada) -> None:
    assert str(tipo) == tipo.value
