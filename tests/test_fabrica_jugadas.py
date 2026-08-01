import pytest

from piedra_papel_tijeras.models.jugadas.fabrica_jugadas import crear_jugada
from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.papel import Papel
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


@pytest.mark.parametrize(
    ("tipo", "clase_esperada"),
    [
        (TipoJugada.PIEDRA, Piedra),
        (TipoJugada.PAPEL, Papel),
        (TipoJugada.TIJERAS, Tijeras),
    ],
)
def test_crear_jugada_devuelve_la_clase_correspondiente(
    tipo: TipoJugada, clase_esperada: type[Jugada]
) -> None:
    assert isinstance(crear_jugada(tipo), clase_esperada)


def test_crear_jugada_rechaza_un_tipo_invalido() -> None:
    with pytest.raises(TypeError):
        crear_jugada("Piedra")  # type: ignore[arg-type]
