from ..tipo_jugada import TipoJugada
from .jugada import Jugada


class Papel(Jugada):
    """Jugada papel, que vence a piedra."""

    @property
    def tipo(self) -> TipoJugada:
        """Devuelve el tipo de la jugada."""
        return TipoJugada.PAPEL

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la jugada."""
        return self.tipo.value

    @property
    def _vence_a_tipo(self) -> TipoJugada:
        """Devuelve el tipo de jugada al que vence."""
        return TipoJugada.PIEDRA

