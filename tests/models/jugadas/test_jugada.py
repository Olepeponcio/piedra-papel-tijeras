import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada


def test_jugada_no_puede_instanciarse_directamente() -> None:
    with pytest.raises(TypeError):
        Jugada()  # type: ignore[abstract]

