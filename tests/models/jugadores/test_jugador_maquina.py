from random import Random
from typing import cast
from unittest.mock import Mock

import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.papel import Papel
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


@pytest.fixture
def jugador() -> JugadorMaquina:
    return JugadorMaquina()


def test_conserva_el_nombre_predeterminado(jugador: JugadorMaquina) -> None:
    assert jugador.nombre == "IA-Player"


def test_conserva_un_nombre_personalizado() -> None:
    jugador = JugadorMaquina("CPU")

    assert jugador.nombre == "CPU"


def test_devuelve_la_representacion_textual_correcta(
    jugador: JugadorMaquina,
) -> None:
    assert str(jugador) == "Nombre: IA-Player"


def test_seleccionar_tipo_usa_el_generador_inyectado() -> None:
    generador = Mock(spec=Random)
    generador.choice.return_value = TipoJugada.PAPEL
    jugador = JugadorMaquina(generador=cast(Random, generador))

    resultado = jugador._seleccionar_tipo()

    assert resultado is TipoJugada.PAPEL
    generador.choice.assert_called_once_with(tuple(TipoJugada))


@pytest.mark.parametrize(
    ("tipo", "clase_esperada"),
    [
        (TipoJugada.PIEDRA, Piedra),
        (TipoJugada.PAPEL, Papel),
        (TipoJugada.TIJERAS, Tijeras),
    ],
)
def test_elegir_jugada_devuelve_la_clase_correspondiente(
    tipo: TipoJugada,
    clase_esperada: type[Jugada],
) -> None:
    generador = Mock(spec=Random)
    generador.choice.return_value = tipo
    jugador = JugadorMaquina(generador=cast(Random, generador))

    resultado = jugador.elegir_jugada()

    assert isinstance(resultado, clase_esperada)
