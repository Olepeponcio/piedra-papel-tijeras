from enum import Enum


class TipoJugada(Enum):
    """Tipos de jugada permitidos."""

    PIEDRA = "Piedra"
    PAPEL = "Papel"
    TIJERAS = "Tijeras"

    def __str__(self) -> str:
        return self.value
