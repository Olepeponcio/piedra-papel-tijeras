from ..tipo_jugada import TipoJugada
from .jugada import Jugada
from .papel import Papel
from .piedra import Piedra
from .tijeras import Tijeras

_CONSTRUCTORES: dict[TipoJugada, type[Jugada]] = {
    TipoJugada.PIEDRA: Piedra,
    TipoJugada.PAPEL: Papel,
    TipoJugada.TIJERAS: Tijeras,
}


def crear_jugada(tipo: TipoJugada) -> Jugada:
    """Crea la jugada concreta asociada al tipo indicado."""
    if not isinstance(tipo, TipoJugada):
        raise TypeError("Tipo debe ser una instancia de TipoJugada")

    return _CONSTRUCTORES[tipo]()
