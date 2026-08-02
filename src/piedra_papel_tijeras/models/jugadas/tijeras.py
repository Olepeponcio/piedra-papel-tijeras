from ..tipo_jugada import TipoJugada
from .jugada import Jugada


class Tijeras(Jugada):
    """Jugada tijeras, que vence a papel.
    Hereda metodos:
        vence_a(self, otra_jugada)->bool:
        __str__(self)->str:
    """

    @property
    def tipo(self) -> TipoJugada:
        """Devuelve el tipo de la jugada."""
        return TipoJugada.TIJERAS

    @property
    def _vence_a_tipo(self) -> TipoJugada:
        """Devuelve el tipo de jugada al que vence.
        método privado de clase usado por vence_a(otra_jugada:TipoJugada) heredado de clase Jugada
        """
        return TipoJugada.PAPEL
