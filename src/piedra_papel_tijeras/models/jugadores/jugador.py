from abc import ABC, abstractmethod
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada
from piedra_papel_tijeras.models.jugadas.jugada import Jugada
from piedra_papel_tijeras.models.jugadas.fabrica_jugadas import crear_jugada


class Jugador(ABC):
    def __init__(self, nombre: str) -> None:
        """inicializa el nombre
        args:
          nombre: str
        """
        self.nombre = nombre

    @abstractmethod
    def _seleccionar_tipo(self) -> TipoJugada:
        """devuelve el tipo de jugada seleccionado"""

    def elegir_jugada(self) -> Jugada:
        """devuelve un objeto de la clase Jugada según la seleccion fijada"""
        return crear_jugada(self._seleccionar_tipo())
