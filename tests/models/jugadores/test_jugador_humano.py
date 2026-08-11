import pytest

from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.papel import Papel
from piedra_papel_tijeras.models.jugadas.piedra import Piedra
from piedra_papel_tijeras.models.jugadas.tijeras import Tijeras
from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


@pytest.fixture
def jugador() -> JugadorHumano:
    return JugadorHumano("Ana")


def test_conserva_el_nombre_al_construir_el_jugador(jugador: JugadorHumano) -> None:
    assert jugador.nombre == "Ana"


def test_jugador_humano_devuelve_la_cadena_correcta(jugador: JugadorHumano) -> None:
    assert str(jugador) == "Nombre: Ana"


def test_utiliza_jugador_como_nombre_predeterminado() -> None:
    assert JugadorHumano().nombre == "Jugador"


def test_no_permite_elegir_jugada_sin_seleccion(jugador: JugadorHumano) -> None:
    with pytest.raises(RuntimeError, match="todavía no ha seleccionado"):
        jugador.elegir_jugada()


def test_devuelve_el_tipo_registrado(jugador: JugadorHumano) -> None:
    jugador.registrar_seleccion(TipoJugada.PAPEL)

    assert jugador._seleccionar_tipo() is TipoJugada.PAPEL


def test_rechaza_un_tipo_no_valido(jugador: JugadorHumano) -> None:
    with pytest.raises(TypeError, match="TipoJugada"):
        jugador.registrar_seleccion("Piedra")  # type: ignore[arg-type]


def test_una_nueva_seleccion_sustituye_a_la_anterior(
    jugador: JugadorHumano,
) -> None:
    jugador.registrar_seleccion(TipoJugada.PIEDRA)
    jugador.registrar_seleccion(TipoJugada.TIJERAS)

    assert jugador._seleccionar_tipo() is TipoJugada.TIJERAS


def test_consumir_la_seleccion_obliga_a_registrar_otra(
    jugador: JugadorHumano,
) -> None:
    jugador.registrar_seleccion(TipoJugada.PIEDRA)
    jugador.elegir_jugada()

    with pytest.raises(RuntimeError, match="todavía no ha seleccionado"):
        jugador.elegir_jugada()


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
    jugador = JugadorHumano("Ana")
    jugador.registrar_seleccion(tipo)

    resultado = jugador.elegir_jugada()

    assert isinstance(resultado, clase_esperada)
