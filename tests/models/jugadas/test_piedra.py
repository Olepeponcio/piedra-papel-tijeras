import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.models.jugadas.papel import Papel
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras


# Cada clase puede instanciarse correctamente.
def test_la_clase_puede_instanciarse_correctamente() -> None:
    piedra = Piedra()
    assert isinstance(piedra, Piedra)


@pytest.mark.parametrize(
    ("tipo", "valor_esperado"),
    [(TipoJugada.PIEDRA, "Piedra")],
)


# cada instancia expone su `tipo` y `nombre` correspondientes.
def test_la_instancia_expone_su_tipo_y_nombre_correspondiente(
    tipo: TipoJugada, valor_esperado: str
) -> None:
    assert tipo.value == valor_esperado


# Cada jugada vence a la jugada definida por sus reglas.
def test_cada_jugada_vence_segun_sus_reglas_definidas() -> None:
    assert Piedra().vence_a(Tijeras())


# Cada jugada pierde frente a la jugada correspondiente.
def test_cada_jugada_pierde_frente_a_la_jugada_correspondiente() -> None:

    assert not Piedra().vence_a(Papel())


# Cada jugada empata con otra instancia del mismo tipo.
def test_jugada_empata_contra_otra_jugada() -> None:
    jugada_empate = Piedra()
    jugada = Piedra()

    assert not jugada.vence_a(jugada_empate) and jugada.tipo == jugada_empate.tipo
