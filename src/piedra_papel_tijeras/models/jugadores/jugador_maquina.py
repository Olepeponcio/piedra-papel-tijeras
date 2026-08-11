from random import Random

from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class JugadorMaquina(Jugador):
    """contrato IA selecciona el tipo de jugada de manera aleaotrizada
    hereda elegir_jugada()->Jugada"""

    def __init__(
        self, nombre: str = "IA-Player", generador: Random | None = None
    ) -> None:
        super().__init__(nombre)

        self._jugadas: tuple[TipoJugada, ...] = tuple(TipoJugada)
        self._generador = generador or Random()

    def _seleccionar_tipo(self) -> TipoJugada:
        """Devuelve un tipo de jugada seleccionado aleatoriamente."""
        return self._generador.choice(self._jugadas)

    # hereda metodo elegir_jugada que usa _seleccionar_tipo
