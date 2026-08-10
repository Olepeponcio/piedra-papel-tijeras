from collections.abc import Callable

import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.papel import Papel
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras
from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


@pytest.fixture
def jugador() -> JugadorHumano:
    return JugadorHumano("Ana", lambda: TipoJugada.PIEDRA)


def test_conserva_el_nombre_al_construir_el_jugador(jugador: JugadorHumano) -> None:
    assert jugador.nombre == "Ana"


def test_jugador_humano_devuelve_la_cadena_correcta(jugador: JugadorHumano) -> None:
    assert str(jugador) == "Nombre: Ana"


def test_seleccionar_tipo_utiliza_el_selector_inyectado() -> None:
    llamadas = 0

    def selector() -> TipoJugada:
        nonlocal llamadas
        llamadas += 1
        return TipoJugada.PAPEL

    jugador = JugadorHumano("Ana", selector)

    resultado = jugador._seleccionar_tipo()

    assert resultado is TipoJugada.PAPEL
    assert llamadas == 1


@pytest.mark.parametrize(
    ("tipo", "clase_esperada"),
    [
        (TipoJugada.PIEDRA, Piedra),
        (TipoJugada.PAPEL, Papel),
        (TipoJugada.TIJERAS, Tijeras),
    ],
)
def test_elegir_jugada_devuelve_jugada_concreta_correspondiente(
    tipo: TipoJugada,
    clase_esperada: type[Jugada],
) -> None:
    selector: Callable[[], TipoJugada] = lambda: tipo
    jugador = JugadorHumano("Ana", selector)

    resultado = jugador.elegir_jugada()

    assert isinstance(resultado, clase_esperada)
