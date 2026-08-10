from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.resultado import Resultado


class Partida:
    """Coordina una ronda entre el jugador humano y la máquina."""

    def __init__(
        self,
        jugador_humano: Jugador,
        jugador_maquina: Jugador,
    ) -> None:
        self.jugador_humano = jugador_humano
        self.jugador_maquina = jugador_maquina

    def jugar(self) -> Resultado:
        """Ejecuta una ronda y devuelve el resultado para el jugador humano."""
        jugada_humana = self.jugador_humano.elegir_jugada()
        jugada_maquina = self.jugador_maquina.elegir_jugada()

        if jugada_humana.tipo is jugada_maquina.tipo:
            return Resultado.EMPATE

        if jugada_humana.vence_a(jugada_maquina):
            return Resultado.VICTORIA

        return Resultado.DERROTA
