from piedra_papel_tijeras.models.jugadores.jugador import Jugador
from piedra_papel_tijeras.models.tipo_jugada import TipoJugada


class JugadorHumano(Jugador):
    """contrato Jugador. Recibe la seleccion de jugada por input
    del usuario. hereda elegir_jugada()->Jugada"""

    def __init__(self, nombre: str) -> None:
        super().__init__(nombre)

    # def _seleccionar_tipo(self) -> TipoJugada:
    #     """devuelve el tipo de jugada seleccionado"""
