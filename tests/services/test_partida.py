import pytest

from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.resultado import Resultado
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.services.partida import Partida


@pytest.mark.parametrize(
    ("tipo_humano", "tipo_maquina", "resultado_esperado"),
    [
        (TipoJugada.PIEDRA, TipoJugada.TIJERAS, Resultado.VICTORIA),
        (TipoJugada.PIEDRA, TipoJugada.PAPEL, Resultado.DERROTA),
        (TipoJugada.PIEDRA, TipoJugada.PIEDRA, Resultado.EMPATE),
    ],
)
def test_partida_resuelve_resultado_desde_la_perspectiva_humana(
    tipo_humano: TipoJugada,
    tipo_maquina: TipoJugada,
    resultado_esperado: Resultado,
) -> None:
    humano = JugadorHumano("Ana", lambda: tipo_humano)
    maquina = JugadorMaquina()
    maquina._seleccionar_tipo = lambda: tipo_maquina  # type: ignore[method-assign]
    partida = Partida(humano, maquina)

    resultado = partida.jugar()

    assert resultado is resultado_esperado
