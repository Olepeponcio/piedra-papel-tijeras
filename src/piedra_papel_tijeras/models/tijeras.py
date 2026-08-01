from .jugada import Jugada
from .tipo_jugada import TipoJugada


class Tijeras(Jugada):
    """clase de tipo_jugada.TIJERAS. vence a tipo_jugada.PAPEL"""

    tipo__jugada = TipoJugada.TIJERAS
    vence_a_tipo = TipoJugada.PAPEL
