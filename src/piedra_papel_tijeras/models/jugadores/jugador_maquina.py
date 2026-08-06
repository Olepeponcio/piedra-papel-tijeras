from random import Random


from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class JugadorMaquina(Jugador):
    """contrato IA selecciona el tipo de jugada de manera aleaotrizada
    hereda elegir_jugada()->Jugada"""

    def __init__(self, nombre: str = "IA-Player") -> None:
        super().__init__(nombre)

    # def _seleccionar_tipo(self) -> TipoJugada:
    #     """devuelve el tipo de jugada seleccionado"""
