from .jugada import Jugada
from .tipo_jugada import TipoJugada


class Tijeras(Jugada):
    """clase de tipo_jugada.TIJERAS. vence a tipo_jugada.PAPEL

    Implementa metodos abastractos como propiedades:
         tipo(self)->TipoJugada

         nombre(self) -> TipoJugada

         _vence_a_tipo(self) -> TipoJugada

     hereda metodos:
         vence_a(self, otra: Jugada) -> bool:

         def __str__(self) -> str
    """

    @property
    def tipo(self) -> TipoJugada:
        """Devuelve el tipo de la jugada"""
        return TipoJugada.TIJERAS

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la jugada."""
        return self.tipo.value

    @property
    def _vence_a_tipo(self) -> TipoJugada:
        """devuelve el tipo de jugada al que vence"""
        return TipoJugada.PAPEL
