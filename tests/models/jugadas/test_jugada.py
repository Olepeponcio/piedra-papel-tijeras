import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras


@pytest.fixture
def jugada():
    return Piedra()


@pytest.fixture
def jugada_empate():
    return Piedra()


@pytest.fixture
def otra_jugada():
    return Tijeras()


def test_jugada_no_puede_instanciarse_directamente() -> None:
    with pytest.raises(TypeError):
        Jugada()  # type: ignore[abstract]


# `vence_a()` devuelve `True` cuando la jugada vence a la recibida.
def test_jugada_vence_a(jugada: Jugada, otra_jugada: Jugada) -> None:
    assert jugada.vence_a(otra_jugada)


# `vence_a()` devuelve `False` ante una derrota o un empate.
def test_jugada_pierde_contra(otra_jugada: Jugada, jugada: Jugada) -> None:
    """invierto el orden de entrada de los argumentos para determinar la derrota"""
    assert jugada.vence_a(jugada) is False


# `vence_a()` devuelve `False` ante una derrota o un empate.
def test_jugada_empata_contra_otra_jugada(
    jugada: Jugada, jugada_empate: Jugada
) -> None:
    assert jugada.vence_a(jugada_empate) is False and jugada.tipo == jugada_empate.tipo


# `vence_a()` rechaza valores que no sean instancias de `Jugada`.
def test_jugada_vence_a_rechaza_valores_incorrectos(jugada: Jugada) -> None:
    with pytest.raises(TypeError, match="Otra debe ser una instancia de Jugada"):
        jugada.vence_a("tijeras")  # type: ignore[arg-type]


# - La representación textual de una jugada coincide con su tipo.
def test_representacion_textual_jugada_coincide_con_su_tipo(jugada: Jugada) -> None:
    assert str(jugada.tipo) == str(jugada.tipo)
