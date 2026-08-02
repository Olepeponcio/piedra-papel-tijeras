import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras


@pytest.fixture
def jugada():
    return Piedra()


@pytest.fixture
def jugada_vencida():
    return Tijeras()


def test_jugada_no_puede_instanciarse_directamente() -> None:
    with pytest.raises(TypeError):
        Jugada()  # type: ignore[abstract]


# `vence_a()` devuelve `True` cuando la jugada vence a la recibida.
def test_jugada_vence_a(jugada: Jugada, jugada_vencida: Jugada) -> None:
    assert jugada.vence_a(jugada_vencida)
