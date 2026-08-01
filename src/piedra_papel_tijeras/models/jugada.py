from abc import ABC, abstractmethod
from tipo_jugada import TipoJugada


class Jugada(ABC):
    """Contrato común para las jugadas del juego."""

    @property
    @abstractmethod
    def tipo(self) -> TipoJugada:
        """Devuelve el tipo de la jugada"""

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Devuelve el nombre de la jugada."""

    @property
    @abstractmethod
    def _vence_a_tipo(self) -> TipoJugada:
        """devuelve el tipo de jugada al que vence"""

    def vence_a(self, otra: Jugada) -> bool:
        """Indica si esta jugada vence a otra."""

        if not isinstance(otra, Jugada):
            raise TypeError("Otra debe ser una instancia de Jugada")

        return otra.tipo is self._vence_a_tipo

    def __str__(self) -> str:
        """Devuelve la representación textual de la jugada."""
        return str(self.tipo)
