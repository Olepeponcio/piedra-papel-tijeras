from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.resultado import Resultado
from piedra_papel_tijeras.models.resultado_ronda import ResultadoDeLaRonda


class Partida:
    """Coordina una ronda entre el jugador humano y la máquina."""

    def __init__(
        self,
        jugador_humano: Jugador,
        jugador_maquina: Jugador,
    ) -> None:
        self._jugador_humano = jugador_humano
        self._jugador_maquina = jugador_maquina

    def jugar(self) -> ResultadoDeLaRonda:
        """Ejecuta una ronda y devuelve el objeto instanciado resultado de la ronda para el jugador humano."""
        jugada_humana = self._jugador_humano.elegir_jugada()
        jugada_maquina = self._jugador_maquina.elegir_jugada()
        # asigna el valor de la clase Resultado que recibirá la ventana_de_juego para asignar imagen
        resultado = (
            Resultado.EMPATE
            if jugada_humana.tipo is jugada_maquina.tipo
            else (
                Resultado.VICTORIA
                if jugada_humana.vence_a(jugada_maquina)
                else Resultado.DERROTA
            )
        )

        return ResultadoDeLaRonda(jugada_humana, jugada_maquina, resultado)
