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


# Conserva el nombre recibido al construir el jugador
def test_conserva_el_nombre_al_construir_el_jugador(jugador: JugadorHumano) -> None:
    assert jugador.nombre == "Ana"


# el objeto devuelve la cadena de texto correcta
def test_jugador_humano_devuelve_la_cadena_correcta(jugador: JugadorHumano) -> None:
    assert str(jugador) == "Nombre: Ana"


# Convierte piedra, papel y tijeras en su `TipoJugada` correspondiente.
@pytest.mark.parametrize(
    ("entrada", "tipo_esperado"),
    [
        ("Piedra", TipoJugada.PIEDRA),
        ("Papel", TipoJugada.PAPEL),
        ("Tijeras", TipoJugada.TIJERAS),
    ],
)
def test_convierte_entrada_en_tipo_jugada_correspondiente(
    jugador: JugadorHumano,
    monkeypatch: pytest.MonkeyPatch,
    entrada: str,
    tipo_esperado: TipoJugada,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: entrada)

    resultado = jugador._seleccionar_tipo()

    assert resultado is tipo_esperado


@pytest.mark.parametrize(
    ("entrada", "tipo_esperado"),
    [
        ("  PIEDRA  ", TipoJugada.PIEDRA),
        (" papel ", TipoJugada.PAPEL),
        ("\tTiJeRaS\n", TipoJugada.TIJERAS),
    ],
)
def test_acepta_mayusculas_y_espacios_exteriores(
    jugador: JugadorHumano,
    monkeypatch: pytest.MonkeyPatch,
    entrada: str,
    tipo_esperado: TipoJugada,
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: entrada)

    resultado = jugador._seleccionar_tipo()

    assert resultado is tipo_esperado


def test_rechaza_entrada_invalida_y_vuelve_a_solicitarla(
    jugador: JugadorHumano,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entradas = iter(["lagarto", "piedra"])
    solicitudes: list[str] = []

    def simular_input(mensaje: str) -> str:
        solicitudes.append(mensaje)
        return next(entradas)

    monkeypatch.setattr("builtins.input", simular_input)

    resultado = jugador._seleccionar_tipo()

    assert resultado is TipoJugada.PIEDRA
    assert len(solicitudes) == 2


def test_tras_entrada_invalida_devuelve_tipo_de_la_siguiente_valida(
    jugador: JugadorHumano,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entradas = iter(["entrada inválida", "papel"])

    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = jugador._seleccionar_tipo()

    assert resultado is TipoJugada.PAPEL


@pytest.mark.parametrize(
    ("entrada", "clase_esperada"),
    [
        ("piedra", Piedra),
        ("papel", Papel),
        ("tijeras", Tijeras),
    ],
)
def test_elegir_jugada_devuelve_jugada_concreta_correspondiente(
    jugador: JugadorHumano,
    monkeypatch: pytest.MonkeyPatch,
    entrada: str,
    clase_esperada: type[Jugada],
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: entrada)

    resultado = jugador.elegir_jugada()

    assert isinstance(resultado, clase_esperada)
