from collections.abc import Callable

from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class JugadorHumano(Jugador):
    """Jugador cuyo tipo de jugada procede de un selector externo."""

    def __init__(
        self,
        nombre: str,
        selector_tipo: Callable[[], TipoJugada],
    ) -> None:
        super().__init__(nombre)
        self._selector_tipo = selector_tipo

    def _seleccionar_tipo(self) -> TipoJugada:
        """Devuelve el tipo proporcionado por el selector configurado."""
        return self._selector_tipo()
