import pytest

from piedra_papel_tijeras.models.jugadores.jugador_humano import JugadorHumano
from piedra_papel_tijeras.models.jugadores.jugador_maquina import JugadorMaquina
from piedra_papel_tijeras.models.resultado import Resultado
from piedra_papel_tijeras.models.resultado_ronda import ResultadoDeLaRonda
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
def test_partida_devuelve_resultado_completo_de_la_ronda(
    tipo_humano: TipoJugada,
    tipo_maquina: TipoJugada,
    resultado_esperado: Resultado,
) -> None:
    jugador_humano = JugadorHumano()
    jugador_humano.registrar_seleccion(tipo_humano)

    jugador_maquina = JugadorMaquina()
    jugador_maquina._seleccionar_tipo = (  # type: ignore[method-assign]
        lambda: tipo_maquina
    )

    partida = Partida(
        jugador_humano=jugador_humano,
        jugador_maquina=jugador_maquina,
    )

    resultado_ronda = partida.jugar()

    assert isinstance(resultado_ronda, ResultadoDeLaRonda)
    assert resultado_ronda.jugada_humana.tipo is tipo_humano
    assert resultado_ronda.jugada_maquina.tipo is tipo_maquina
    assert resultado_ronda.resultado is resultado_esperado
