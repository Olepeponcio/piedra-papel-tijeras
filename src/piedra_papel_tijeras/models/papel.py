from .jugada import Jugada
from .tipo_jugada import TipoJugada


class Papel(Jugada):
    """clase de tipo_jugada.PAPEL. vence a tipo_jugada.PIEDRA"""

    @property
    def tipo(self) -> TipoJugada:
        return TipoJugada.PAPEL

    @property
    def vence_a_tipo(self) -> TipoJugada:
        return TipoJugada.PIEDRA
