from .jugada import Jugada
from .tipo_jugada import TipoJugada


class Piedra(Jugada):
    """clase de tipo_jugada.PIEDRA. vence a tipo_jugada.TIJERAS"""

    tipo__jugada = TipoJugada.PIEDRA
    vence_a_tipo = TipoJugada.TIJERAS
